# Тут сделано кривовато, но можно исправить! :)


python cli_gen_code/main.py gen-models -json-schema-dir="G:\\Programms\\PyCharmProjects\\VKinternProjectfastapi\\different_documents\\test.json" -out-dir="G:\\Programms\\PyCharmProjects\\VKinternProjectfastapi\\rest\\models\\test\\"
# -json-schema-dir = Путь до вашего .json файла
# -out-dir = project\\rest\\models\\тип документа (создается папка)\\ Сохранять сюда все новые модели
python cli_gen_code/main.py gen-rest -models="G:\\Programms\\PyCharmProjects\\VKinternProjectfastapi\\rest\\models\\engine\\" -rest-routes="G:\\Programms\\PyCharmProjects\\VKinternProjectfastapi\\rest\\routes\\engine\\"
# -models = Путь до папки в которой находится pydantic модель project\\rest\\models\\тип документа (создается папка)\\
# -rest-routes = Путь куда сохраняются эндпоинты \\rest\\routes\\тип документа (создается папка)\\ Сюда сохранять все новые руты

if [ ! -d .git ]; then
    git init
    git remote add main https://github.com/AlLixAI/VKintern # нужный гит репозиторий
fi
git add .
git commit -m "Генерация pydantic моделей и контроллеров"
NEW_TAG=$(date +'%Y%m%d%H%M%S')
git tag $NEW_TAG
git push origin main
git push origin $NEW_TAG
exec $SHELL # можно удалить, если не нужно