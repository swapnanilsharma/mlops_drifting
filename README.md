Grafana START/STOP and PORT

brew services start grafana
brew services stop grafana
http://localhost:3000


Prometheus START/STOP and PORT
brew services start prometheus
brew services stop prometheus
http://localhost:9090


Poetry install
curl -sSL https://install.python-poetry.org | python3 -
poetry new my_project
poetry init
poetry shell
exit
poetry add package_name
poetry remove package_name


brew install python@3.10
poetry env use $(pyenv which python3.10)
poetry shell