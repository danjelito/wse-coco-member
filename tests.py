import config


def test_all_memberships_are_filled(df_clean, student_membership_col):
    """
    All memberships should be filled with no blank.
    """
    expected_memberships_with_st = ["Deluxe", "Go", "Street Talk", "VIP"]
    expected_memberships_without_st = ["Deluxe", "Go", "VIP"]
    unique_memberships = sorted(df_clean[student_membership_col].dropna().unique())
    assert (
        expected_memberships_with_st == unique_memberships
        or expected_memberships_without_st == unique_memberships
    ), f"Membership test failed. Expected {expected_memberships_with_st} or {expected_memberships_without_st}, get {unique_memberships}."


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


def test_cpt_members_in_cpt_area(
    df_clean, is_cpt_col, student_center_col, student_area_col
):
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


def test_one_code_is_one_name(df_clean, code_col, name_col):
    """One code must have one name only."""

    count_multiple = (
        df_clean.groupby(code_col)
        .agg(count_student_name=(name_col, "nunique"))
        .reset_index()
        .loc[lambda df_: df_["count_student_name"] > 1, code_col]
        .tolist()
    )
    assert not count_multiple, f"Some codes have multiple names: {count_multiple}"
