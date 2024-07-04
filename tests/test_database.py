def test_invoke_query(database):
    result = database.invoke_query('SELECT 1')
    assert result == [{'1': 1}]


def test_invoke_commands(database):
    commands = [
        ("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)",),
        ("INSERT INTO test (name) VALUES (:name)", {"name": "Bob"}),
    ]
    database.invoke_commands(commands)
    result = database.invoke_query("SELECT * FROM test")
    assert len(result) == 1
    assert result[0]['name'] == 'Bob'


def test_invoke_file_w_returned_data(database, tmp_path):
    p = tmp_path / 'query.txt'
    p.write_text('SELECT 1')
    result = database.invoke_file(p)
    assert result == [{'1': 1}]


def test_invoke_file_wo_returned_data(database, tmp_path):
    p = tmp_path / 'query.txt'
    p.write_text('CREATE TABLE test2 (id INTEGER PRIMARY KEY, name TEXT)')
    result = database.invoke_file(p)
    assert result is None
