# Starter by tox

- [一般的なパッケージングについて](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [tox](https://tox.wiki/en/4.15.1/installation.html)

## Install Tox

```
$ pip install tox
```

## Initialize project

```
$ mkdir -p starter-by-tox-sample
```

```
$ cd starter-by-tox-sample
$ curl -Lo ./.gitignore https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore
```

```
$ vim pyproject.toml
```

```
$ vim tox.ini
```

```
$ tox
```

## Using cookiecutter

cookiecutterで公開されてるプロジェクトテンプレートを利用するのもありです。

- https://github.com/cookiecutter/cookiecutter

```
$ python -m pip install --user cookiecutter
```

pypackage

```
$ cookiecutter https://github.com/audreyfeldroy/cookiecutter-pypackage.git
```

openstack project

```
$ cookiecutter https://opendev.org/openstack/cookiecutter.git
```
