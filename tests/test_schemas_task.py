from app.schemas.task import TaskCreate, TaskUpdate, TaskOut


def test_task_create_schema():
    task = TaskCreate(title="Minha tarefa", description="Descrição")
    assert task.title == "Minha tarefa"
    assert task.description == "Descrição"


def test_task_create_schema_without_description():
    task = TaskCreate(title="Só título")
    assert task.description is None


def test_task_update_schema_partial():
    update = TaskUpdate(description="Nova descrição")
    assert update.title is None
    assert update.description == "Nova descrição"


def test_task_out_schema():
    out = TaskOut(id=1, owner_id=2, title="Título", description="Texto")
    assert out.id == 1
    assert out.owner_id == 2
    assert out.title == "Título"
    assert out.description == "Texto"
