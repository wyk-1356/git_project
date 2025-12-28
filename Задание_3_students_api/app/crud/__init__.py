# Импорт CRUD функций для удобного доступа
from app.crud.student import (
    get_student, get_students, create_student, update_student, delete_student,
    add_student_to_group, remove_student_from_group, get_students_in_group, transfer_student
)

from app.crud.group import (
    get_group, get_groups, create_group, update_group, delete_group
)
