# Pluto Templating Web App

### This web application was designed and built to host a custom template formatter

### The formatter is accepts a template syntax as designed by Pluto VR

#### BUILD INSTRUCTIONS

1. Install docker and docker-compose

- You may find this [link](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04) helpful.
- You may also use pip to install docker-compose

2. Pull this repo to a local directory
3. Ensure that you are in the same directory as the docker-compose files
4. Ensure that ports 3000 and 5000 are available
5. After you ensure that the above are complete, build and deploy app with the one of these cmds:
   - production: `docker-compose -f docker-compose-prod.yml up --build -d`
   - development: `docker-compose up --build -d`

#### Tests

You may run tests with this cmd: `docker-compose exec api pytest`

#### Syntax Overview

##### Variable Declaration

Variable declaration takes the form of !<VAR_NAME>=<VALUE>
Variable declaration must adhere exactly to this structure, else the app will convey an error

##### Variable Interpolation

Variable interpolation takes the form of @<VAR_NAME>
Variable declaration must adhere exactly to this structure, else the app will convey an error
If a variable is not declared, the app will convey an error

##### Variable Concatention

Variable contentation takes the form of @{<VAR_NAME>}<TEXT>
Of course, variables must be declared to use them

##### Escaping The @ Symbol

To escape the @ symbol, precede it with one @ symbol

#### SAMPLE TEMPLE

```
!name1=Wade
!name2=Watts
!avatar=Parzival
!salutation=Dear aka
101 IOI Plaza
!company=Innovative Online Industries
!product=OASIS Haptic Suit
!phone=1-800-SUPPORT
Columbus, OH 43123

@salutation,

Thank you for your interest in @{product}s. Unfortunately, we are not taking orders of the @product until early next year.

@name1, if you have any more questions about our products, email us at support@@ioi.com, tweet to @@ioi_support, or call us @@ @phone.

Thank you @avatar for being a valued member of the OASIS!!

Customer Support
@company
```
