"""
Database model v5 relationships

Pack <> PackLocalized
"""

from arcaea_offline.constants.enums import ArcaeaLanguage
from arcaea_offline.database.models import ModelsV5Base, Pack, PackLocalized


class TestPackRelationships:
    @staticmethod
    def init_db(session):
        ModelsV5Base.metadata.create_all(session.bind)

    def test_localized_objects(self, db_session):
        self.init_db(db_session)

        pack_id = "test_pack"
        name_en = "Test Pack"
        description_en = "Travel through common database models\nfrom the unpopular framework 'Arcaea Offline'\ntogether with an ordinary partner '∅'."

        pack = Pack(
            id=pack_id,
            name=name_en,
            description=description_en,
        )

        pkid_ja = 1
        description_ja = "普通のパートナー「∅」と一緒に、\n不人気フレームワーク「Arcaea Offline」より、\n一般的なデータベース・モデルを通過する。"
        pack_localized_ja = PackLocalized(
            pkid=pkid_ja,
            id=pack_id,
            lang=ArcaeaLanguage.JA.value,
            name=None,
            description=description_ja,
        )

        pkid_zh_hans = 2
        description_zh_hans = "与平凡的「∅」一起，\n在没人用的「Arcaea Offline」框架里，\n一同探索随处可见的数据库模型。"
        pack_localized_zh_hans = PackLocalized(
            pkid=pkid_zh_hans,
            id=pack_id,
            lang=ArcaeaLanguage.ZH_HANS.value,
            name=None,
            description=description_zh_hans,
        )

        db_session.add_all([pack, pack_localized_ja])
        db_session.commit()

        assert len(pack.localized_objects) == len([pack_localized_ja])

        assert pack_localized_ja.parent.description == pack.description

        # relationships should be viewonly
        new_pack = Pack(
            id=f"{pack_id}_new",
            name="NEW",
            description="new new pack",
        )
        db_session.add(new_pack)

        pack_localized_ja.parent = new_pack
        pack.localized_objects.append(pack_localized_zh_hans)
        db_session.commit()

        assert pack_localized_ja.parent == pack
        assert len(pack.localized_objects) == 1
