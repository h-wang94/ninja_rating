from bs4 import BeautifulSoup
import urllib2
import os
import re

def instr_ratings_grab(soup): #FOR ONE COURSE ONLY.
  instr_ratings = soup.find_all('a', 'no-decoration')
  profs = []
  for ratings in instr_ratings:
    prof_soup = read_site("http://www.ninjacourses.com/" + ratings['href'])
    profs_span = prof_soup.find_all('span', 'item fn')
    for prof_name in profs_span:
      profs.append(prof_name.string + " " + ratings.string + " --")
  return profs # in a specific course

def course_ratings_grab(link):
  course_ratings = []
  noratings = "0 ratings & Not rated " #MSG to show no ratings for class
  soup = read_site(link)
  
  instr_ratings = instr_ratings_grab(soup)
  # overall_ratings: average rating for class
  overall_rating = soup.find_all('div', 'float-left value')
  # number_ratings: number of ratings for the class
  number_ratings = soup.find_all('span', 'count')
  # If rating does exist...
  if (len(overall_rating) > 0):
    content = overall_rating[0].string + "[" + number_ratings[0].string + "] "
    for x in range(len(instr_ratings)):
      content += instr_ratings[x] + " "
    course_ratings.append(content)
  else: # If doesn't exist, use norating
    content = ""
    for y in range(len(instr_ratings)):
      content += instr_ratings[y]
    course_ratings.append(noratings + " " + content)
  return course_ratings

def course_info_grab(soup, file):
  url = "http://www.ninjacourses.com"
  ratings = "#ratings"
  li = soup.find_all('li')[5:]
  ## Remove top LI tags that dont relate to classes
  course_desc = course_desc_grab(li)
  course_name = course_name_grab(li)
  course_links = course_links_grab(li)
  course_ratings = []
  for links in course_links: #For each COURSE, navigate through the link.
    links = url + links + ratings
    course_ratings.append(course_ratings_grab(links))
  file_write(file, course_name, course_desc, course_ratings)

def course_desc_grab(li):
  course_desc = [lis.a.next_element.next_element for lis in li]
  return course_desc

def course_name_grab(li):
  course_name = [lis.a.get_text() for lis in li]
  return course_name

def course_links_grab(li):
  course_links = [lis.a['href'] for lis in li]
  return course_links

def dept_list_grab(soup, file):
  dept_list = []
  depts = soup.find_all('li')[8:]
  dept_links = course_links_grab(depts)
  file.write("Course Name, Course Desc, Num of Ratings, Overall Rating, Prof Name, Prof Rating\n")
  for links in dept_links:
    links = "http://www.ninjacourses.com" + links
    course_info_grab(read_site(links), file)
  file.close()
  return

def read_site(link):
  """ Open and read the site and extract ALL contents to soup to allow for
  parsing """
  url = urllib2.urlopen(link)
  content = url.read()
  soup = BeautifulSoup(content)
  return soup

def file_open():
  """ Define a file to be written to. Then, all contents needed will be
  placed in the file. 
  """
  ### Input file name to write to.
  file_name = raw_input("What file would you like to write to? ")
  if os.path.isfile(file_name):
    confirmation = raw_input("File already exists. Would you like to overwrite? Y/N\n")
    if (confirmation == "Y" or confirmation == "y"):
      ### Removes file if confirmed
      os.remove(file_name)
    ### Opens file and appends results
  file = open(file_name, 'a')
  return file

def file_write(file, course_name, course_desc, course_ratings):
  file.write("Course Name - Course Desc, OverallRating[Num of Ratings], Prof Name, Prof Rating")
  file.write("***--------------------****\n")
  file.write("\n")
  for x in range(len(course_name)):
    content = course_name[x] + " " + course_desc[x] + " " + course_ratings[x][0]
    file.write(content + '\n\n')
  file.close() #COMMENT OUT ONLY WHEN USING ALL DEPARTMENTS

def dept_prompt():
  DEPT_LIST = ["AEROSPC", "AFRICAM", "AFRKANS", "AGR CHM", "A,RESEC", "ALTAIC", "AMERSTD", "AHMA", "ANTHRO", "AST", "ARABIC", "ARCH", "ASAMST", "ASIANST", "ASTRON", "BANGLA", "XMBA", "BIO ENG", "BIOLOGY", "BIOPHY", "BUDDSTD", "CATALAN", "CELTIC", "CHM ENG", "CHEM", "CHICANO", "CHINESE", "CY PLAN", "CIV ENG", "CLASSIC", "COG SCI", "COLWRIT", "COMPBIO", "COM LIT", "CGB", "COMPSCI", "CRIT TH", "CUNEIF", "DEMOG", "DEV STD", "PHDBA", "DUTCH", "EPS", "EA LANG", "EAEURST", "ECON", "EDUC", "EGYPT", "EL ENG", "ENE,RES", "ENGIN", "ENGLISH", "ENV DES", "ENVECON", "ESPM", "ETH STD", "ETH GRP", "EURA ST", "EWMBA", "FILIPN", "FILM", "FOLKLOR", "FRENCH", "MBA", "GWS", "GEOG", "GERMAN", "GMS", "GPP", "GSPDP", "GREEK", "HMEDSCI", "HEBREW", "HIN-URD", "HISTORY", "HISTART", "ILA", "IND ENG", "INFO", "INTEGBI", "ISF", "IAS", "IRANIAN", "ITALIAN", "JAPAN", "JEWISH", "JOURN", "KHMER", "KOREAN", "LD ARCH", "LAN PRO", "LATIN", "LATAMST", "LAW", "LEGALST", "LGBT", "L & S", "LINGUIS", "MALAY/I", "MASSCOM", "MFE", "MAT SCI", "MATH", "MEC ENG", "MEDIAST", "MEDIAST", "MED ST", "M E STU", "MIL AFF", "MIL SCI", "MCELLBI", "MUSIC", "NSE", "NATAMST", "NAT RES", "NAV SCI", "NE STUD", "NEUROSC", "NWMEDIA","NUC ENG", "NUSCTX", "OPTOM", "PACS", "PERSIAN", "PHILOS", "PHYS ED", "PHYSICS", "PLANTBI", "POLECON", "POL SCI", "PORTUG", "ART", "PSYCH", "PB HLTH", "PUB POL", "PUNJABI", "RELIGST", "RHETOR", "SANSKR", "SCANDIN", "SCMATHE", "SEMITIC", "SLAVIC", "SOC WEL", "SOCIOL", "S,SEASN", "S ASIAN", "SEASIAN", "SPANISH", "STAT", "TAGALG", "TAMIL", "TELUGU", "THAI", "THEATER", "TIBETAN", "TURKISH", "UGIS", "UGBA", "VIETNMS", "VIS SCI", "VIS STD", "YIDDISH"]
  input = raw_input("What department do you want to get information from? Ex: COMPSCI\n")
  while (input.upper() not in DEPT_LIST):
    print "Error! " + input + " department doesn't exist! Input another one!\n"
    input = raw_input("What department do you want to get information from? Ex: COMPSCI\n")
  return input

url_to_open = "http://www.ninjacourses.com/explore/1/department/"
dept = dept_prompt()
file = file_open()
soup = read_site(url_to_open + dept)
course_info_grab(soup, file)
