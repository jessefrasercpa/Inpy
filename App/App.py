import click
from rich.table import Table
from rich.console import Console
from Rentables.utils import registerDefaultRates
from Discounts import registerDefaultDiscounts
from API import API
from .utils import (
    AddOnRepo,
    RoomRepo
)


SUCCESS_COLOUR = "green"
ERROR_COLOUR   = "red"

api = API()

registerDefaultRates(api)
registerDefaultDiscounts(api)

addOnRepo = AddOnRepo(api)
roomRepo  = RoomRepo(api)

console = Console()


@click.group()
def cli():

    pass


@cli.group()
def addOns():

    pass

@cli.group()
def rooms():

    pass


def getClickType(type_: str):

    return {
            "int": int,
            "float": float,
            "str": str,
            "bool": bool
    }.get(type_, str)


def buildClickType(type_: str, constraints: dict):

    if "choices" in constraints:

        return click.Choice(constraints["choices"])
    
    inner = getClickType(type_)

    if inner is int:

        return click.InRange(
            min=constraints.get("min"),
            max=constraints.get("max")
        )
    
    if inner is float:

        return click.FloatRange(
            min=constraints.get("min"),
            max=constraints.get("max")
        )
    
    return inner


def parseListType(type_: str):

    return type_[type_.find("[") + 1:type_.find("]")]


def promptParams(paramsJSON):

    values = {}

    for param in paramsJSON:

        name         = param["name"]
        type_        = param["type"]
        description = param.get("description", "")
        constraints = param.get("constraints", {}).copy()

        promptDescription = f"\t{name}"

        if description:

            promptDescription += f" ({description})"

        if type_.startswith("list"):

            clickType = buildClickType(parseListType(type_), constraints)

            items = []
            count = 1

            console.print(f"{promptDescription} | Enter one per line, blank to finish . . .")

            while True:

                try:

                    value = click.prompt(
                        f"\t\t[{count}]",
                        type=str,
                        default="",
                        show_default=False
                    )

                    if value == "":

                        break
                    
                    value = clickType.convert(value, None, None)

                    items.append(value)
                    count += 1

                except click.BadParameter as e:

                    console.print(f"[{ERROR_COLOUR}][ERROR][/{ERROR_COLOUR}] {e}")

            values[name] = items

            continue

        clickType = buildClickType(type_, constraints)

        while True:

            try:

                value        = click.prompt(promptDescription, type=clickType)
                values[name] = value

                break

            except click.BadParameter as e:

                console.print(f"[{ERROR_COLOUR}][ERROR][/{ERROR_COLOUR}] {e}")

    return values


# ============================================================================ #
# Add-Ons                                                                      #
# ============================================================================ #


@addOns.command("new")
def newAddOn():

    name = click.prompt("Add-On Name")

    rateType       = click.prompt(
        "Select Rate Type",
        type=click.Choice(api.listRates())
    )
    metaRateParams = api.getRateParams(rateType)
    rateParams     = promptParams(metaRateParams)

    try:

        addOn = addOnRepo.add(
            {
                "id": name.lower().replace(" ", "_"),
                "name": name,
                "rate": {
                    "rateType": rateType,
                    "params": rateParams
                }
            }
        )

        console.print(
            f"\n[{SUCCESS_COLOUR}][SUCCESS][/{SUCCESS_COLOUR}] " \
            f"Add-On '{addOn.name}' " \
            f"(id: {addOn.id}) " \
            f"successfully created\n"
        )

        table = Table(
            title=f"Add-On: {addOn.name}",
            show_header=False,
        )
    
        table.add_column("Field")
        table.add_column("Value")

        table.add_row("ID", addOn.id)
        table.add_row("Name", addOn.name)
        table.add_row("Rate", addOn.rate.name)

        console.print(table)

    except ValueError as e:

        console.print(f"\n[{ERROR_COLOUR}][ERROR][/{ERROR_COLOUR}] {e}")


@addOns.command("delete")
def deleteAddOn():

    id    = click.prompt("Add-On id")

    try:

        addOn = addOnRepo.get(id)

        addOnRepo.delete(id)

        console.print(
            f"\n[{SUCCESS_COLOUR}][SUCCESS][/{SUCCESS_COLOUR}] " \
            f"Add-On '{addOn.name}' " \
            f"(id: {addOn.id}) " \
            f"successfully deleted"
        )

    except ValueError as e:

        console.print(f"\n[{ERROR_COLOUR}][ERROR][/{ERROR_COLOUR}] {e}")


@addOns.command("ls")
def listAddOns():

    addOns = addOnRepo.ls()

    if not addOns:

        console.print(
            f"\n[{ERROR_COLOUR}][ERROR][/{ERROR_COLOUR}] " \
            f"No Add-Ons to list"
        )

        return
    
    console.print(
        f"\n[{SUCCESS_COLOUR}][SUCCESS][/{SUCCESS_COLOUR}] " \
        f"Add-Ons:\n"
    )

    table = Table()

    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Rate")

    for addOn in addOns:

        table.add_row(
            addOn.id,
            addOn.name,
            addOn.rate.name
        )

    console.print(table)


# ============================================================================ #


# ============================================================================ #
# Rooms                                                                        #
# ============================================================================ #


def printRoom(room):

    table = Table(title=f"Room: {room.name}", show_header=False)

    table.add_column("Field")
    table.add_column("Value")

    table.add_row("ID", room.id)
    table.add_row("Name", room.name)
    table.add_row("Rate", room.rate.name)
    
    if room.addOns:

        table.add_row("Add-On", ", ".join([addOn.name for addOn in room.addOns]))

    console.print(table)


@rooms.command("new")
def newRoom():

    name = click.prompt("Room Name")

    rateType       = click.prompt("Select Rate Type", type=click.Choice(api.listRates()))
    metaRateParams = api.getRateParams(rateType)
    rateParams     = promptParams(metaRateParams)

    addOnsObjs    = addOnRepo.ls()
    addOnNames    = [addOn.name for addOn in addOnsObjs]
    addOnNameToAddOn = {addOn.name: addOn for addOn in addOnsObjs}

    addOns = []
    count  = 1

    console.print(
        f"Select Add-Ons ({addOnNames}) | Enter one per line, blank to finish . . ."
    )

    while True:

        try:

            addOnName = click.prompt(
                f"\t\t[{count}]",
                default="",
                show_default=False
            )

            if addOnName == "":

                break

            addOnName = click.Choice(addOnNames).convert(addOnName, None, None)
            addOn     = addOnNameToAddOn[addOnName]

            addOns.append(
                {
                    "id": addOn.id,
                    "name": addOn.name,
                    "rate": {
                        "rateType": addOn.rate.name,
                        "params": addOn.rate.params
                    }
                }
            )

            count += 1

        except click.BadParameter as e:

            console.print(f"[{ERROR_COLOUR}][ERROR][/{ERROR_COLOUR}] {e}")


    try:

        room = roomRepo.add(
            {
                "id": name.lower().replace(" ", "_"),
                "name": name,
                "rate": {
                    "rateType": rateType,
                    "params": rateParams
                },
                "addOns": addOns
            }
        )

        console.print(
            f"\n[{SUCCESS_COLOUR}][SUCCESS][/{SUCCESS_COLOUR}] " \
            f"Room '{room.name}' " \
            f"(id: {room.id}) " \
            f"successfully created\n"
        )

        printRoom(room)

    except ValueError as e:

        console.print(f"\n[{ERROR_COLOUR}][ERROR][/{ERROR_COLOUR}] {e}")


@rooms.command("delete")
def deleteRoom():

    id    = click.prompt("Room id")

    try:

        room = roomRepo.get(id)

        roomRepo.delete(id)

        console.print(
            f"\n[{SUCCESS_COLOUR}][SUCCESS][/{SUCCESS_COLOUR}] " \
            f"Room '{room.name}' " \
            f"(id: {room.id}) " \
            f"successfully deleted"
        )

    except ValueError as e:

        console.print(f"\n[{ERROR_COLOUR}][ERROR][/{ERROR_COLOUR}] {e}")


@rooms.command("ls")
def listRooms():

    rooms = roomRepo.ls()

    if not rooms:

        console.print(
            f"\n[{ERROR_COLOUR}][ERROR][/{ERROR_COLOUR}] " \
            f"No Rooms to list"
        )

        return
    
    console.print(
        f"\n[{SUCCESS_COLOUR}][SUCCESS][/{SUCCESS_COLOUR}] " \
        f"Rooms:\n"
    )

    table = Table()

    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Rate")
    table.add_column("Add-Ons")

    for room in rooms:

        table.add_row(
            room.id,
            room.name,
            room.rate.name,
            ", ".join([addOn.name for addOn in room.addOns])
        )

    console.print(table)


# ============================================================================ #


if __name__ == "__main__":

    cli()
