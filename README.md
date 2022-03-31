## Space Way Web

Server side (Web and API) for [Space Way](https://github.com/YariKartoshe4ka/Space-Way/) game


### Developing

In principle, the site doesn't need to be changed, and the code was opened in order to quickly identify vulnerabilities by GitHub's kind-hearted flatterers, so before starting development and making changes, please open the issue so that in the discussion we can make sure that this is necessary

#### Stack

To work successfully with the code, you need to know the following technologies

###### Front end

JavaScript with [jQuery](https://jquery.com/), [SCSS](https://sass-lang.com/)

###### Back end

Python 3, [Django](https://www.djangoproject.com/)

#### Setup

The project uses a Makefile, so you can start development very quickly (if you work on Linux)

```sh
# Clone repo
git clone https://github.com/YariKartoshe4ka/Space-Way-Web.git
cd Space-Way-Web

# Install dependencies
make deps

# Prepare project
make setup
nano app/.env # Change variables
make db

# Run site
python manage.py runserver
```
