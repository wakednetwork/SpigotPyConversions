from dev.magicmq.pyspigot import PySpigot as ps
from org.bukkit.event.block import Action
from org.bukkit.event.player import PlayerInteractEvent
from org.bukkit.event.entity import EntitySpawnEvent
from org.bukkit.entity import Player, Snowball, Boat
from org.bukkit import Bukkit, ChatColor
from org.bukkit.scheduler import BukkitRunnable
from java.util import UUID

# Anti-crash player tracking dictionary
anticrash_data = {}

# Configurable thresholds for crash detection
lever_threshold = 5
snowball_threshold = 50
boat_threshold = 30
lever_reset_time = 40  # 40 ticks (2 seconds)

# On right-click lever event
def on_lever_click(event):
    if isinstance(event.getPlayer(), Player):
        player = event.getPlayer()
        if event.getAction() == Action.RIGHT_CLICK_BLOCK and event.getClickedBlock().getType().name() == "LEVER":
            player_uuid = str(player.getUniqueId())

            # Increment player's lever count
            if player_uuid not in anticrash_data:
                anticrash_data[player_uuid] = {'levers': 0}
            anticrash_data[player_uuid]['levers'] += 1

            # Detect crash attempt
            if anticrash_data[player_uuid]['levers'] > lever_threshold:
                event.setCancelled(True)
                notify_admins(f"&c{player.getName()} is trying to crash the server with levers!")

            # Reset lever count after 2 seconds
            reset_lever_count(player_uuid)

def reset_lever_count(player_uuid):
    def reset_task():
        anticrash_data[player_uuid]['levers'] = 0

    ps.scheduler.runTaskLater(reset_task, lever_reset_time)

# On snowball spawn event
def on_snowball_spawn(event):
    if isinstance(event.getEntity(), Snowball):
        snowball_count = len([entity for entity in event.getEntity().getNearbyEntities(50, 50, 50) if isinstance(entity, Snowball)])
        if snowball_count > snowball_threshold:
            for entity in event.getEntity().getNearbyEntities(200, 200, 200):
                if isinstance(entity, Snowball):
                    entity.remove()
            nearest_player = get_nearest_player(event.getEntity().getLocation())
            if nearest_player:
                notify_admins(f"&c{nearest_player.getName()} is trying to crash the server with snowballs!")
            event.setCancelled(True)

# On boat spawn event
def on_boat_spawn(event):
    if isinstance(event.getEntity(), Boat):
        boat_count = len([entity for entity in event.getEntity().getNearbyEntities(50, 50, 50) if isinstance(entity, Boat)])
        if boat_count > boat_threshold:
            for entity in event.getEntity().getNearbyEntities(50, 50, 50):
                if isinstance(entity, Boat):
                    entity.remove()
            nearest_player = get_nearest_player(event.getEntity().getLocation())
            if nearest_player:
                notify_admins(f"&c{nearest_player.getName()} is trying to crash the server with boats or minecarts!")
            event.setCancelled(True)

# Notify admins with permission "op"
def notify_admins(message):
    for player in Bukkit.getOnlinePlayers():
        if player.hasPermission("op"):
            player.sendMessage(ChatColor.translateAlternateColorCodes('&', message))

# Helper function to get the nearest player to a location
def get_nearest_player(location):
    nearest_player = None
    nearest_distance = float('inf')
    for player in Bukkit.getOnlinePlayers():
        distance = player.getLocation().distance(location)
        if distance < nearest_distance:
            nearest_player = player
            nearest_distance = distance
    return nearest_player

# Register the event listeners
ps.listener.registerListener(on_lever_click, PlayerInteractEvent)
ps.listener.registerListener(on_snowball_spawn, EntitySpawnEvent)
ps.listener.registerListener(on_boat_spawn, EntitySpawnEvent)
