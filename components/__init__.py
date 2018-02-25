import components.adorablesconfig
import components.callbackqueries
import components.choseninline
import components.commands
import components.otheravatars


def register(dp):
    components.commands.register(dp)
    components.adorablesconfig.register(dp)
    components.otheravatars.register(dp)
    components.callbackqueries.register(dp)
    components.choseninline.register(dp)

