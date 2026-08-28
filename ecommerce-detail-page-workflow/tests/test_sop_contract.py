import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class SopContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.workflow = (SKILL_ROOT / "references" / "workflow.md").read_text(
            encoding="utf-8"
        )
        cls.templates = (SKILL_ROOT / "references" / "output_templates.md").read_text(
            encoding="utf-8"
        )
        cls.connected = (
            SKILL_ROOT / "references" / "connected_reference_count_workflow.md"
        ).read_text(encoding="utf-8")

    def test_single_complete_source_photo_is_sufficient(self) -> None:
        combined = self.skill + self.workflow
        self.assertIn("一张能完整展示产品的清晰图片", combined)
        self.assertIn("有真实多角度图时", combined)
        self.assertIn("不得强迫用户补拍", combined)

    def test_white_background_stage_expands_assets_with_evidence_boundaries(self) -> None:
        combined = self.skill + self.workflow + self.templates
        self.assertIn("白底素材扩展包", combined)
        self.assertIn("多机位", combined)
        self.assertIn("细节特写", combined)
        self.assertIn("AI 衍生可确认角度", combined)
        self.assertIn("不得虚构背面", combined)
        self.assertIn("隐藏结构", combined)

    def test_missing_reference_routes_to_xiaohongshu_research(self) -> None:
        combined = self.skill + self.workflow + self.connected
        self.assertIn("小红书", combined)
        self.assertIn("公开互动信号", combined)
        self.assertIn("不是平台官方排名", combined)

    def test_generation_uses_a_binary_error_correction_gate(self) -> None:
        combined = self.skill + self.workflow
        self.assertIn("纠错门槛", combined)
        self.assertIn("字体崩溃", combined)
        self.assertIn("画面崩溃", combined)
        self.assertIn("未出现字体崩溃或画面崩溃就直接输出", combined)
        self.assertIn("最多自动纠错 1 次", combined)

    def test_complete_delivery_keeps_lossless_assembly_contract(self) -> None:
        combined = self.skill + self.workflow
        self.assertIn("stitch_long_page.py", combined)
        self.assertIn("PIXEL_MATCH", combined)
        self.assertIn("独立分屏", combined)
        self.assertIn("完整长图", combined)

    def test_default_route_is_lean_and_heavy_work_is_conditional(self) -> None:
        combined = self.skill + self.workflow
        self.assertIn("默认使用 LEAN", combined)
        self.assertIn("最小素材组", combined)
        self.assertIn("不得扩展为更多前置素材", combined)
        self.assertIn("6–8 屏", combined)

    def test_research_and_process_documents_are_bounded(self) -> None:
        combined = self.skill + self.workflow
        self.assertIn("一次聚焦调研", combined)
        self.assertIn("默认不创建过程报告", combined)
        self.assertIn("紧凑执行清单", combined)

    def test_visual_quality_is_left_to_the_user(self) -> None:
        combined = self.skill + self.workflow
        self.assertIn("画面具体的效果和质量交给用户判断", combined)
        self.assertIn("不自动评价", combined)
        self.assertIn("设计感", combined)
        self.assertIn("高级感", combined)
        self.assertIn("构图偏好", combined)

    def test_main_images_do_not_enter_full_detail_page_pipeline(self) -> None:
        combined = self.skill + self.workflow
        self.assertIn("主图快捷路线", combined)
        self.assertIn("不进入完整详情页流程", combined)

    def test_revision_only_reopens_affected_pages(self) -> None:
        combined = self.skill + self.workflow
        self.assertIn("只重开受影响页面", combined)
        self.assertIn("不得重跑已确认阶段", combined)

    def test_intake_asks_only_for_publish_platform_after_product_image(self) -> None:
        combined = self.skill + self.workflow
        self.assertIn("收到产品图后只询问发布平台", combined)
        self.assertIn("不得批量追问", combined)
        self.assertIn("平台确认后判断产品信息是否充足", combined)

    def test_complete_product_information_skips_research_and_enters_assets(self) -> None:
        combined = self.skill + self.workflow
        self.assertIn("有详情页信息和产品图片", combined)
        self.assertIn("跳过调研", combined)
        self.assertIn("直接进入白底精修和多角度细节生成", combined)

    def test_missing_product_information_requires_copy_confirmation(self) -> None:
        combined = self.skill + self.workflow + self.templates
        self.assertIn("没有产品信息", combined)
        self.assertIn("小红书和其他平台", combined)
        self.assertIn("详情页文案确认稿", combined)
        self.assertIn("交付给用户确认", combined)
        self.assertIn("确认前不得生成白底精修或扩展素材", combined)

    def test_default_asset_pack_is_three_group_images(self) -> None:
        combined = self.skill + self.workflow
        self.assertIn("默认 3 张素材组", combined)
        self.assertIn("白底精修主图", combined)
        self.assertIn("多角度组合图", combined)
        self.assertIn("细节组合图", combined)
        self.assertIn("不逐张等待用户确认", combined)

    def test_downstream_starts_after_confirmed_copy_and_assets(self) -> None:
        combined = self.skill + self.workflow
        self.assertIn("确认文案与素材", combined)
        self.assertIn("6–8 屏策划", combined)
        self.assertIn("Image2 逐屏生成", combined)
        self.assertIn("无损拼接", combined)


if __name__ == "__main__":
    unittest.main()
