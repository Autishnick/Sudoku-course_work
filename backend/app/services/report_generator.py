import datetime
import html as _html


def format_report_as_html(game_list: list):
    """
    Форматує список ігор у HTML-таблицю.
    (Працює зі словниками)
    """
    html = """
    <html>
    <head>
        <title>Sudoku Reports</title>
        <style>
            /* ... (ваші стилі) ... */
        </style>
    </head>
    <body>
        <h1>Completed Games Report</h1>
        <table border='1'>
            <tr>
                <th>Game ID</th>
                <th>Name</th>
                <th>Start Time (UTC)</th>
                <th>End Time (UTC)</th>
                <th>Duration</th>
            </tr>
    """
    
    for game in game_list:
        game_id = game.get("id")
        # escape names to avoid breaking HTML if they contain special chars
        raw_name = game.get("name")
        game_name = _html.escape(raw_name) if raw_name else "(Unnamed)"
        start_time = game.get("start_time")
        end_time = game.get("end_time")

        # support both datetime objects and ISO strings
        if hasattr(start_time, "strftime"):
            start_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(start_time, str):
            start_str = start_time
        else:
            start_str = "N/A"

        if hasattr(end_time, "strftime"):
            end_str = end_time.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(end_time, str):
            end_str = end_time
        else:
            end_str = "N/A"

        duration = "N/A"
        try:
            if end_time and start_time:
                duration_delta = end_time - start_time
                duration = str(duration_delta)
        except Exception:
            duration = "N/A"

        html += f"""
            <tr>
                <td>{game_id}</td>
                <td>{game_name}</td>
                <td>{start_str}</td>
                <td>{end_str}</td>
                <td>{duration}</td>
            </tr>
        """
    
    html += "</table></body></html>"
    return html