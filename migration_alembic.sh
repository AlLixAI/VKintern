if [ ! -d "migrations" ]; then
    echo "Не удалось найти каталог миграций. Убедитесь, что вы находитесь в корневом каталоге проекта."
    exit 1
fi

echo "Введите описание для миграции:"
read DESCRIPTION

alembic revision --autogenerate -m "$DESCRIPTION"

alembic upgrade head

echo "Миграции успешно выполнены."
exec $SHELL # можно удалить, если не нужно