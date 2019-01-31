def get_formatted_price(price):
    """
    Get formatted price from cents amount.
    Example: price=4000 => $40.00
    """
    return '${0:.2f}'.format(price / 100)
