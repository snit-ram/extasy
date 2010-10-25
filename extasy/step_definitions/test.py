import extasy.selenium
from pycukes import *

@When( 'I cuto a bola' )
def cuto_a_bola(context):
    extasy.selenium.getDriver().start_test()
    extasy.selenium.getDriver().page_open( 'http://www.google.com.br/' )
    extasy.selenium.getDriver().wait_for_page()
    extasy.selenium.getDriver().stop_test()
    