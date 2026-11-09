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
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 40px; background: #f9f9f9; color: #333; }
            h1 { color: #222; }
            table { border-collapse: collapse; width: 100%; background: #fff; box-shadow: 0 2px 8px rgba(0,0,0,0.06); border-radius: 8px; overflow: hidden; }
            th, td { padding: 12px 16px; text-align: left; border-bottom: 1px solid #eee; }
            th { background-color: #ffd600; color: #222; font-weight: 600; }
            tr:hover { background-color: #fafafa; }
            .empty { color: #888; font-style: italic; }
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
        raw_name = game.get("name")
        game_name = _html.escape(raw_name) if raw_name else "(Unnamed)"
        start_time = game.get("start_time")
        end_time = game.get("end_time")

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
                duration = str(duration_delta).split(".")[0]
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
    
    if not game_list:
        html += """
            <tr>
                <td colspan="5" class="empty" style="text-align: center; padding: 25px;">
                    Немає завершених ігор / No completed games yet.
                </td>
            </tr>
        """
    
    html += "</table></body></html>"
    return html