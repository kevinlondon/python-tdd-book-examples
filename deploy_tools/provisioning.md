Provisioning a New Site
=======================

## Required packages:

* nginx
* Py 3
* git
* pip
* virtualenv

eg on Ubuntu:

    sudo pip3 install requirmenets
    
or

    sudo apt-get install nginx git python3 python3-pip
    sudo pip3 install virtualenv

## Nginx Virtual Host Config

* see nginx.template.conf
* replace SITENAME with, eg, staging.kevinlondon.com

## Upstart Job

* See gunicorn-upstart.template.conf
* Replace SITENAME with, eg, staging.kevinlondon.com

## Folder Structure
Assume we have a user account at /home/www

/home/www
--- sites
    ---- SITENAME
        ---- database
        ---- source
        ---- static
        ---- virtualenv
