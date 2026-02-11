import click
from rich.table import Table
from rich.console import Console
from Rentables.utils import registerDefaultRates
from Discounts import registerDefaultDiscounts
from API import API
from .utils import AddOnRepo


FIELD_STYLE  = "dim"
RATE_COLOUR  = "red"
ADDON_COLOUR = "white"

SUCCESS_COLOUR = "green"
ERROR_COLOUR   = "red"

api = API()

registerDefaultRates(api)
registerDefaultDiscounts(api)

addOnRepo = AddOnRepo(api)

console = Console()


@click.group()
def cli():

    pass


@cli.group()
def addOns():

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
            count = 0

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


def getRateTable(rate):

    rateTable = Table(
        show_header=False,
        box=None
    )
    
    rateTable.add_column("Field", style=FIELD_STYLE)
    rateTable.add_column("Value", style=RATE_COLOUR)

    rateTable.add_row("Name", rate.name)

    for key, value in rate.params.items():

        rateTable.add_row(key, str(value))

    return rateTable


def printAddOn(addOn):

    table = Table(
        title=f"Add-On: {addOn.name}",
        show_header=False,
        border_style=ADDON_COLOUR
    )
    
    table.add_column("Field", style=FIELD_STYLE)
    table.add_column("Value", style=ADDON_COLOUR)

    table.add_row("ID", addOn.id)
    table.add_row("Name", addOn.name)
    table.add_row("Rate", getRateTable(addOn.rate))

    console.print(table)


@addOns.command("new")
def newAddOn():

    name = click.prompt("Add-On Name")

    rateType       = click.prompt("Select Rate Type", type=click.Choice(api.listRates()))
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
            f"Add-On [{ADDON_COLOUR}]'{addOn.name}'[/{ADDON_COLOUR}] " \
            f"(id: {addOn.id}) " \
            f"succefully created\n"
        )

        printAddOn(addOn)

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
            f"Add-On [{ADDON_COLOUR}]'{addOn.name}'[/{ADDON_COLOUR}] " \
            f"(id: {addOn.id}) " \
            f"succefully deleted"
        )

    except ValueError as e:

        console.print(f"\n[{ERROR_COLOUR}][ERROR][/{ERROR_COLOUR}] {e}")


@addOns.command("ls")
def listAddOns():

    addOns = addOnRepo.ls()

    if not addOns:

        console.print(
            f"[{ERROR_COLOUR}][ERROR][/{ERROR_COLOUR}] " \
            f"No [{ADDON_COLOUR}]Add-Ons to[/{ADDON_COLOUR}] list"
        )

        return
    
    console.print(
        f"\n[{SUCCESS_COLOUR}][SUCCESS][/{SUCCESS_COLOUR}] " \
        f"[{ADDON_COLOUR}]Add-Ons[/{ADDON_COLOUR}]:\n"
    )

    table = Table(
        border_style=ADDON_COLOUR,
        show_lines=True
    )

    table.add_column("ID", style=FIELD_STYLE)
    table.add_column("Name")
    table.add_column("Rate")

    for addOn in addOns:

        table.add_row(
            addOn.id,
            addOn.name,
            getRateTable(addOn.rate)
        )

    console.print(table)


if __name__ == "__main__":

    cli()
