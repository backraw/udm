# ../udm/menus.py

"""Provides the `CloseButtonPagedMenu` which calls a callback when a player decides to close the menu."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Menus
from menus.radio import BUTTON_CLOSE
from menus.radio import PagedRadioMenu


# =============================================================================
# >> CLOSE BUTTON PAGED MENU
# =============================================================================
class CloseButtonPagedMenu(PagedRadioMenu):
    """Class used to call a callback when a player decides to close the menu."""

    def __init__(self, close_callback, **kwargs):
        """Object initialization."""
        super().__init__(**kwargs)

        # Store the close callback
        self._close_callback = close_callback

    def _select(self, player_index, choice_index):
        """Call the close callback if the close button has been selected."""
        if choice_index == BUTTON_CLOSE:
            self._close_callback(player_index)

        # Continue the base class routine
        return super()._select(player_index, choice_index)
