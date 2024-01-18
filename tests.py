import config

def test_all_memberships_are_filled(df_clean):
    """
    All memberships should be filled with no blank.
    """
    assert sorted(df_clean["student_membership"].unique()) == ["Deluxe", "GO", "VIP"]


def test_all_centers_are_filled(df_clean):
    """
    All centers should be filled with no blank.
    """

    from itertools import chain

    centers_nested = list(config.map_areas.values())
    centers = list(chain(*centers_nested))

    unmapped = set(df_clean["student_center"].unique()) - set(centers)
    assert not unmapped, f"{unmapped} is incorrectly mapped"


def test_all_areas_are_filled(df_clean):
    """
    All areas should be filled with no blank.
    """

    from itertools import chain

    areas = list(config.map_areas.keys())

    unmapped = set(df_clean["student_area"].unique()) - set(areas)
    assert not unmapped, f"{unmapped} is incorrectly mapped"


def test_cpt_members_in_cpt_area(df_clean):
    """
    All corporate should be in corporate center and area.
    """
    assert (
        not (
            df_clean.loc[df_clean["is_cpt"], ["student_center", "student_area"]]
            != "Corporate"
        )
        .sum()
        .sum()
    )


def test_noncpt_members_in_noncpt_area(df_clean):
    """
    All corporate should be in corporate center and area.
    """
    assert (
        not (
            df_clean.loc[~(df_clean["is_cpt"]), ["student_center", "student_area"]]
            == "Corporate"
        )
        .sum()
        .sum()
    )