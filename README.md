# mac-sensors-aws

## Description
This is currently a simple python program that collects cpu temperature and fan speed data by using the `istats` utility.  
It's a little hacky, but until I find the time to make it nicer, such is life.

## Why
I wanted to see how it would be to quickly (a couple hours) create a program that could read sensor data and save/send it.  
I also wanted to play around with AWS some more, so this program can either save data to a CSV file or send it to AWS IoT Analytics. Documentation on how to set this up in AWS will come in the future.

## Considerations
The .py file is just a straight dump from a Jupyter Notebook (.ipynb), and I haven't tested it yet, so it may not do anything particularly useful.  
Setting the data retreival frequency too high will cause issues where it won't actually do it that fast and will end up extending the data gathering time.

## istats
istats is a ruby gem whose github can be found here:
<a href="https://github.com/Chris911/iStats">https://github.com/Chris911/iStats</a>  
Installation is as simple as `gem install ruby`.

## Future Development
I do hope to find or create a nice python library that not only gives cpu temperatures and fan speeds, but other nice sensor data such as clock speed, gpu data, etc.

Created by Jonathan Osborne Contreras  TheJonWZ@Gmail.com