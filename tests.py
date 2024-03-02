import config


def test_all_memberships_are_filled(df_clean, student_membership_col):
    """
    All memberships should be filled with no blank.
    """
    assert sorted(df_clean[student_membership_col].unique()) == [
        "Deluxe",
        "Go",
        "VIP",
    ], "test_all_memberships_are_filled failed"


def test_all_centers_are_filled(df_clean, student_center_col):
    """
    All centers should be filled with no blank.
    """

    from itertools import chain

    centers_nested = list(config.map_areas.values())
    centers = list(chain(*centers_nested))

    unmapped = set(df_clean[student_center_col].unique()) - set(centers)
    assert (
        not unmapped
    ), f"test_all_centers_are_filled failed, {unmapped} is incorrectly mapped"


def test_all_areas_are_filled(df_clean, student_area_col):
    """
    All areas should be filled with no blank.
    """
    unmapped = set(df_clean[student_area_col].unique()) - set(config.map_areas.keys())
    assert (
        not unmapped
    ), f"test_all_areas_are_filled failed, {unmapped} is incorrectly mapped"


def test_cpt_members_in_cpt_area(df_clean, is_cpt_col, student_center_col, student_area_col):
    """
    All corporate should be in corporate center and area.
    """
    assert (
        not (
            df_clean.loc[df_clean[is_cpt_col], [student_center_col, student_area_col]]
            != "Corporate"
        )
        .sum()
        .sum()
    ), "test_cpt_members_in_cpt_area failed"


def test_noncpt_members_in_noncpt_area(df_clean, is_cpt_col):
    """
    All corporate should be in corporate center and area.
    """
    assert (
        not (
            df_clean.loc[~(df_clean[is_cpt_col]), ["student_center", "student_area"]]
            == "Corporate"
        )
        .sum()
        .sum()
    ), "test_noncpt_members_in_noncpt_area"
