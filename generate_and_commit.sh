python cli_gen_code/main.py gen-models -json-schema-dir="G:\\Programms\\PyCharmProjects\\VKinternProjectfastapi\\different_documents\\engine.json" -out-dir="G:\\Programms\\PyCharmProjects\\VKinternProjectfastapi\\rest\\models\\engine\\"
# -json-schema-dir = Путь до вашего .json файла
# -out-dir = project\\rest\\models\\тип документа (создается папка)\\ Сохранять сюда все новые модели
python cli_gen_code/main.py gen-rest -models="G:\\Programms\\PyCharmProjects\\VKinternProjectfastapi\\rest\\models\\engine\\" -rest-routes="G:\\Programms\\PyCharmProjects\\VKinternProjectfastapi\\rest\\routes\\engine\\"
# -models = Путь до папки в которой находится pydantic модель project\\rest\\models\\тип документа (создается папка)\\
# -rest-routes = Путь куда сохраняются эндпоинты \\rest\\routes\\тип документа (создается папка)\\ Сюда сохранять все новые руты

git init
git add .
git commit -m "Генерация pydantic моделей и контроллеров"
NEW_TAG=$(date +'%Y%m%d%H%M%S')
git tag $NEW_TAG
git push origin $NEW_TAG
exec $SHELL