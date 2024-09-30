from dev.magicmq.pyspigot import PySpigot as ps
from org.bukkit import Bukkit
from org.bukkit import ChatColor
from org.bukkit.entity import Player

# Command to send an announcement with title and optional subtitle
def announce_command(sender, label, args):
    if len(args) == 0:
        sender.sendMessage(ChatColor.RED + "Usage: /announce <message>")
        return True

    # Join arguments as subtitle
    subtitle = ' '.join(args)

    # Title string with color codes
    title = "&x&F&B&C&4&0&0&lA&x&F&B&B&D&0&0&lN&x&F&C&B&7&0&0&lN&x&F&C&B&0&0&0&lO&x&F&C&A&9&0&0&lU&x&F&D&A&2&0&0&lN&x&F&D&9&C&0&0&lC&x&F&E&9&5&0&0&lE&x&F&E&8&E&0&0&lM&x&F&E&8&7&0&0&lE&x&F&F&8&1&0&0&lN&x&F&F&7&A&0&0&lT!"

    # Translate color codes
    colored_title = ChatColor.translateAlternateColorCodes('&', title)
    colored_subtitle = ChatColor.translateAlternateColorCodes('&', subtitle)

    # Send the title and subtitle to all online players
    for player in Bukkit.getOnlinePlayers():
        player.sendTitle(colored_title, colored_subtitle, 10, 70, 20)

    return True

# Register the announce command
ps.command.registerCommand(announce_command, 'announce', 'Announce a message with a title', '/announce <message>', ['announce'])
