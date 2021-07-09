# String that is used to find the window handle.
window_name = 'LDPlayer'

# HP threshold coordinate on the screen. Pixel color is checked at this exact location.
ooc_hp_pos = [297, 970]
# Mana threshold coordinate on the screen. Pixel color is checked at this exact location.
ooc_mana_pos = [298, 987]

# The number of enemies that must be found in order to stop the search algorithm.
enemy_number = 3

# Attack skill coordinate on the screen
attack_pos = [148, 879]

# Player sprite location in the center of the screen
p_c_loc = [254, 491]
# Area around the player srite in the center of the screen to be ignored
p_c_loc_offset_pos = 60
p_c_loc_offset_neg = 40

# Player sprite location at the bottom of the screen
p_b_loc = [254, 865]
# Area around the player srite at the bottom of the screen to be ignored
p_b_loc_offset = 60