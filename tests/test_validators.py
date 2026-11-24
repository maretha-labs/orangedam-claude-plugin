"""Unit tests for all OrangeDAM plugin Python validators and hygiene checker."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True

REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_DIR = REPO_ROOT / "plugin"
SKILLS_DIR = PLUGIN_DIR / "skills"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


hygiene_mod = load_module(REPO_ROOT / "scripts/check_plugin_hygiene.py", "check_plugin_hygiene")
wb_mod = load_module(SKILLS_DIR / "ol-implementation-blueprint/scripts/validate_workbook.py", "validate_workbook")
pkg_mod = load_module(SKILLS_DIR / "ol-implementation-blueprint/scripts/assemble_onboarding_package.py", "assemble_pkg")
meta_mod = load_module(SKILLS_DIR / "ol-metadata-schema/scripts/validate_metadata_schema.py", "validate_metadata")
tag_mod = load_module(SKILLS_DIR / "ol-taxonomy-tags/scripts/validate_tag_tree.py", "validate_tags")
emb_mod = load_module(SKILLS_DIR / "ol-embedded-metadata/scripts/validate_embedded_mappings.py", "validate_embedded")
fld_mod = load_module(SKILLS_DIR / "ol-folder-structure/scripts/validate_folder_tree.py", "validate_folders")
sec_mod = load_module(SKILLS_DIR / "ol-security-permissions/scripts/audit_permissions.py", "audit_permissions")
mig_mod = load_module(SKILLS_DIR / "ol-migration-cutover/scripts/validate_migration_plan.py", "validate_migration")


def test_plugin_hygiene_passes_on_actual_bundle():
    res = hygiene_mod.check_plugin(PLUGIN_DIR, REPO_ROOT)
    assert res["errors"] == [], f"Unexpected hygiene errors: {res['errors']}"
    assert res["warnings"] == [], f"Unexpected hygiene warnings: {res['warnings']}"
    assert res["status"] == "pass"
    assert res["file_count"] <= 512


def test_metadata_template_passes_and_catches_errors(tmp_path: Path):
    tpl = SKILLS_DIR / "ol-metadata-schema/assets/metadata-fields-template.csv"
    ok = meta_mod.validate_metadata_csv(tpl)
    assert ok["errors"] == []
    assert ok["row_count"] == 12

    bad_csv = tmp_path / "bad_meta.csv"
    bad_csv.write_text(
        "Field Name in OrangeDAM,Field Type,Tag Type,Orange Logic API Field Name,Operator,Image\n"
        "Brand,Multi-Valued Field - Apply Tag only if it exists already,N/A,acme.Brand,++=,x\n"
        "Brand,InvalidType,,acme.Brand,BADOP,x\n",
        encoding="utf-8",
    )
    bad = meta_mod.validate_metadata_csv(bad_csv)
    assert bad["status"] == "fail"
    assert any("requires a Tag Type" in e for e in bad["errors"])
    assert any("contradicting" in e for e in bad["errors"])
    assert any("duplicate Field Name" in e for e in bad["errors"])
    assert any("invalid DataTable V2.2 Operator" in e for e in bad["errors"])


def test_tag_tree_template_passes_and_catches_errors(tmp_path: Path):
    tpl = SKILLS_DIR / "ol-taxonomy-tags/assets/tag-tree-template.csv"
    ok = tag_mod.validate_tag_tree(tpl)
    assert ok["errors"] == []
    assert ok["status"] == "pass"

    bad_csv = tmp_path / "bad_tags.csv"
    bad_csv.write_text(
        "Tag Type (Category),Tag Term Level 0,Tag Term Level 1,Tag Term Level 2\n"
        "Regions,,SkippedL0,Deep\n"
        "Regions,EMEA,,\n"
        "Regions,EMEA,,\n"
        "Regions,Bad|Pipe,,\n",
        encoding="utf-8",
    )
    bad = tag_mod.validate_tag_tree(bad_csv)
    assert bad["status"] == "fail"
    assert any("skipped hierarchy level" in e for e in bad["errors"])
    assert any("duplicate taxonomy path" in e for e in bad["errors"])
    assert any("contains '|'" in e for e in bad["errors"])


def test_embedded_metadata_template_passes_and_catches_traps(tmp_path: Path):
    tpl = SKILLS_DIR / "ol-embedded-metadata/assets/embedded-mapping-template.csv"
    ok = emb_mod.validate_embedded_csv(tpl)
    assert ok["errors"] == []
    assert ok["status"] == "pass"

    bad_csv = tmp_path / "bad_emb.csv"
    bad_csv.write_text(
        "Rule #,Create rule?,Priority (OrderNumber),Source Type,Source Field,In COR picker?,Option-list action,Destination Field,Destination Field Type,Direction\n"
        "1,Yes,1,EXIF,CreateDate,Yes,None,CreateDate,Date,Upload\n"
        "2,Yes,1,EXIF,ExposureTime,Yes,None,acme.Shutter,Number,Upload\n"
        "3,Yes,1,EXIF,LensModel,No,None,acme.Lens,Text,Upload\n"
        "4,Yes,1,EXIF,FileSource,No,Add to EXIFFieldsOptionList,Source,Text,Upload\n"
        "5,Yes,1,EXIF,DateTimeOriginal,Yes,None,DocDate,Date,Upload\n"
        "6,Yes,1,IPTC,Application2_DateCreated,Yes,None,DocDate,Date,Upload\n",
        encoding="utf-8",
    )
    bad = emb_mod.validate_embedded_csv(bad_csv)
    assert bad["status"] == "fail"
    assert any("CreateDate" in e for e in bad["errors"])
    assert any("must be Text, not Numeric" in e for e in bad["errors"])
    assert any("EXIFFieldsOptionList" in e for e in bad["errors"])
    assert any("FileSource" in e for e in bad["errors"])
    assert any("duplicate Priority" in e for e in bad["errors"])


def test_folder_tree_template_passes_and_enforces_50k_limit(tmp_path: Path):
    tpl = SKILLS_DIR / "ol-folder-structure/assets/folder-structure-template.csv"
    ok = fld_mod.validate_folder_tree(tpl)
    assert ok["errors"] == []
    assert ok["status"] == "pass"

    bad_csv = tmp_path / "bad_folders.csv"
    bad_csv.write_text(
        "Level 1,Level 2,Level 3,Projected Asset Count\n"
        "Library,MegaDump,,75000\n"
        "Library,,SkippedL2,100\n",
        encoding="utf-8",
    )
    bad = fld_mod.validate_folder_tree(bad_csv)
    assert bad["status"] == "fail"
    assert any("50,000" in e for e in bad["errors"])
    assert any("skips empty Level 2" in e for e in bad["errors"])


def test_security_audit_passes_templates_and_catches_leaks(tmp_path: Path):
    sec_assets = SKILLS_DIR / "ol-security-permissions/assets"
    ok = sec_mod.audit(
        sec_assets / "groups-template.csv",
        sec_assets / "permissions-matrix-template.csv",
        sec_assets / "visibility-classes-template.csv",
    )
    assert ok["errors"] == []
    assert ok["status"] == "pass"

    bad_groups = tmp_path / "groups.csv"
    bad_groups.write_text(
        "Group,Account Type,Custom,Test Account to Impersonate,Parent Groups,Who can add and remove users for this group?\n"
        "GroupA,Security,x,,GroupB,Administrator\n"
        "GroupB,Security,x,,GroupA,Administrator\n",
        encoding="utf-8",
    )
    bad_perms = tmp_path / "perms.csv"
    bad_perms.write_text(
        "On Folder / Asset,Group,Visibility Class,S,M,L,Original,Dwlnd Btn,Find,Edit\n"
        "Library,*UnregisteredUsers,Pending Process,x,,,,x,x,x\n"
        "Library,GroupA,Public,,,,,x,x,\n",
        encoding="utf-8",
    )
    bad = sec_mod.audit(bad_groups, bad_perms, None)
    assert bad["status"] == "fail"
    assert any("circular group inheritance" in e for e in bad["errors"])
    assert any("write/admin permission granted to anonymous" in e for e in bad["errors"])
    assert any("scoped strictly to 'Public'" in e for e in bad["errors"])
    assert any("Show Dwld Btn is enabled without any View" in e for e in bad["errors"])


def test_migration_plan_validator(tmp_path: Path):
    good = tmp_path / "good.json"
    good.write_text(
        json.dumps(
            {
                "target_cloud": "AWS",
                "target_region": "us-east-1",
                "sources": [
                    {
                        "name": "Legacy DAM",
                        "volume_tb": 10.0,
                        "file_count": 120000,
                        "source_cloud": "AWS",
                        "source_region": "us-east-1",
                        "max_assets_in_single_folder": 30000,
                        "extensions": [".jpg", ".png", ".mov", ".pdf"],
                        "has_3d_files": False,
                        "has_zip_files": False,
                        "extension_waivers_reviewed": True,
                        "cutoff_date": "2026-12-31",
                        "mvp_launch_subset": "2026 Published (25k files)",
                        "active_edits_during_migration": True,
                        "delta_cutover_plan": "Incremental sync + 48h freeze",
                        "has_published_links": True,
                        "published_links_plan": "Redirect table updated in CMS",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    ok = mig_mod.validate_migration_plan(good)
    assert ok["status"] == "pass"
    assert ok["errors"] == []

    bad = tmp_path / "bad.json"
    bad.write_text(
        json.dumps(
            {
                "target_cloud": "AWS",
                "target_region": "us-east-1",
                "sources": [
                    {
                        "name": "Live Box",
                        "volume_tb": 5.0,
                        "file_count": 80000,
                        "source_cloud": "GCP",
                        "source_region": "us-central1",
                        "max_assets_in_single_folder": 65000,
                        "extensions": [".jpg", ".exe"],
                        "extension_waivers_reviewed": False,
                        "active_edits_during_migration": True,
                        "has_published_links": True,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    res = mig_mod.validate_migration_plan(bad)
    assert res["status"] == "fail"
    assert any("50,000" in e for e in res["errors"])
    assert any("prohibited/executable" in e for e in res["errors"])
    assert any("delta_cutover_plan" in e for e in res["errors"])
    assert any("published_links_plan" in e for e in res["errors"])
    assert any("cross-cloud" in w for w in res["warnings"])


def test_cross_domain_workbook_and_handoff_assembly(tmp_path: Path):
    # Copy clean templates into a single workbook directory
    (tmp_path / "metadata_fields.csv").write_text(
        (SKILLS_DIR / "ol-metadata-schema/assets/metadata-fields-template.csv").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (tmp_path / "tags.csv").write_text(
        (SKILLS_DIR / "ol-taxonomy-tags/assets/tag-tree-template.csv").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (tmp_path / "folders.csv").write_text(
        (SKILLS_DIR / "ol-folder-structure/assets/folder-structure-template.csv").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (tmp_path / "visibility_classes.csv").write_text(
        (SKILLS_DIR / "ol-security-permissions/assets/visibility-classes-template.csv").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (tmp_path / "groups.csv").write_text(
        (SKILLS_DIR / "ol-security-permissions/assets/groups-template.csv").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (tmp_path / "permissions.csv").write_text(
        (SKILLS_DIR / "ol-security-permissions/assets/permissions-matrix-template.csv").read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    res = wb_mod.validate_directory(tmp_path)
    assert res["errors"] == [], f"Unexpected cross-domain errors: {res['errors']}"
    assert res["status"] == "pass"

    md = pkg_mod.build_handoff_markdown(tmp_path)
    assert "metadata_fields.csv" in md
    assert "permissions.csv" in md
    assert "Impersonation UAT Passed" in md
