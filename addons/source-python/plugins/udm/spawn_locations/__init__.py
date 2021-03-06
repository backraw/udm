# ../udm/spawn_locations/__init__.py

"""Provides spawn point management."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   JSON
import json

# Source.Python Imports
#   Core
from core import GAME_NAME
#   Engines
from engines.server import global_vars
#   Listeners
from listeners import OnLevelInit
#   Mathlib
from mathlib import QAngle
from mathlib import Vector
#   Paths
from paths import PLUGIN_DATA_PATH

# Script Imports
#   Info
from udm.info import info


# =============================================================================
# >> CONSTANTS
# =============================================================================
# Safe distance between spawn points (in units)
SAFE_SPAWN_DISTANCE = 150.0


# =============================================================================
# >> CLASSES
# =============================================================================
class SpawnLocation(Vector):
    """Class used to attach a QAngle to a Vector and provide a JSON representation for the respective locations."""

    def __init__(self, x, y, z, angle):
        """Object initialization."""
        # Call Vector's constructor using the given xyz-coordinates
        super().__init__(x, y, z)

        # Store the QAngle object
        self._angle = angle

    @classmethod
    def from_player_location(cls, player):
        """Return a `SpawnPoint` (subclass) object from a player's location."""
        return cls(player.origin.x, player.origin.y, player.origin.z, player.view_angle)

    def move_player(self, player):
        """Move the player to this spawn point location."""
        player.origin = self
        player.view_angle = self.angle

    @property
    def angle(self):
        """Return the QAngle object."""
        return self._angle

    @property
    def json(self):
        """Return a JSON representation of the `self` and `self.angle`."""
        return {
            'vector': [self.x, self.y, self.z],
            'angle': [self.angle.x, self.angle.y, self.angle.z]
        }


class SpawnLocationManager(list):
    """Class used to provide spawn point managing functionality:

        * load spawn points from a JSON file
        * save spawn points to a JSON file
    """

    # Store the spawn points data path
    path = PLUGIN_DATA_PATH.joinpath(info.name, 'spawn_locations', GAME_NAME)

    def load(self):
        """Load spawn points from the spawn points data file for the current map."""
        # Skip if the file doesn't exist
        if not self.json_file.exists():
            return

        # Read the spawn points data file into memory
        with self.json_file.open() as f:
            contents = json.load(f)

        # Append each entry as a `SpawnPoint` object
        for data in contents:
            self.append(SpawnLocation(*data['vector'], QAngle(*data['angle'])))

    def save(self):
        """Save spawn points to the spawn points data file for the current map."""
        # Skip if we have nothing to save
        if not self:
            return

        # Dump the contents of this list to file
        with self.json_file.open('w') as f:
            json.dump([spawnpoint.json for spawnpoint in self], f, indent=4)

    @property
    def json_file(self):
        """Return the path to the JSON file for the current map."""
        if not self.path.exists():
            self.path.makedirs()

        return self.path.joinpath(f'{global_vars.map_name}.json')


# =============================================================================
# >> PUBLIC GLOBAL VARIABLES
# =============================================================================
# Store a global instance of `_SpawnPoints`
spawn_location_manager = SpawnLocationManager()

# Load all spawn points for the current map
spawn_location_manager.load()


# =============================================================================
# >> LISTENERS
# =============================================================================
@OnLevelInit
def on_level_init(map_name):
    """Reload spawn points."""
    spawn_location_manager.clear()
    spawn_location_manager.load()
