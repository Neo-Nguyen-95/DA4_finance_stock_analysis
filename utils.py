# display visible number
def format_number(num):
    if abs(num) >= 1_000_000_000:
        return f'{num / 1_000_000_000:.1f}B'
    elif abs(num) >= 1_000_000:
        return f'{num / 1_000_000:.1f}M'
    elif abs(num) >= 1_000:
        return f'{num / 1_000:.1f}K'
    else:
        return str(num)