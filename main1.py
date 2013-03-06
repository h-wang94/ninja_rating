from bs4 import BeautifulSoup
import urllib2
import os
import re
"""
def instr_ratings_grab(soup):
  instr_ratings = soup.find_all(text="Previous Instructors")
  instr_ratings = soup.find_all('div', 'ratings-instructor')
  
# print instr_ratings
  
  instr_ratings = soup.find_all('span', 'rating-details-qtip')
  print instr_ratings
  instr_ratings = " ".join(line.strip() for line in instr_ratings[0].get_text().split("\n"))
  instr_ratings = " ".join(line.strip() for line in instr_ratings.split("  "))
  print instr_ratings

  """
def course_ratings_grab(link):
  course_ratings = []
  noratings = "0 ratings & Not rated" #MSG to show no ratings for class
  soup = read_site(link)
  
  # instr_ratings = instr_ratings_grab(soup)
  # overall_ratings: average rating for class
  overall_rating = soup.find_all('div', 'float-left value')
  # number_ratings: number of ratings for the class
  number_ratings = soup.find_all('span', 'count')
  # If rating does exist...
  if (len(overall_rating) > 0):
    content = number_ratings[0].string + " " + overall_rating[0].string
    course_ratings.append(content)
    #print "# of Ratings: " + number_ratings[0].string
    #print "Overall rating: " + overall_rating[0].string
  else: # If doesn't exist, use norating
    course_ratings.append(noratings)
    #print "# Ratings = 0"
    #print "Not rated"
  return course_ratings

def course_info_grab(soup, file):
  url = "http://www.ninjacourses.com"
  ratings = "#ratings"
  li = soup.find_all('li')[5:]
  ## Remove top LI tags that dont relate to classes
  #li = li[5:]
  course_desc = course_desc_grab(li)
  course_name = course_name_grab(li)
  course_links = course_links_grab(li)
  course_ratings = []
  for links in course_links:
    links = url + links + ratings
    course_ratings.append(course_ratings_grab(links))
  file_write(file, course_name, course_desc, course_ratings)
  #print course_desc
  #print course_name
  #print course_links
  #print course_ratings

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
  #depts = soup.find_all('li')[5:] # INCLUDES AC/HONOR/RC
  depts = soup.find_all('li')[8:]
  dept_links = course_links_grab(depts)
  file.write("Course Name, Course Desc, Num of Ratings, Overall Rating\n")
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
  # Comment out only when using ALL DEPARTMENTS
  #file.write("Course Name, Course Desc, Num of Ratings, Overall Rating\n")
  for x in range(len(course_name)):
    content = course_name[x] + " " + course_desc[x] + " " + course_ratings[x][0]
    file.write(content + '\n')
  #file.close() #COMMENT OUT ONLY WHEN USING ALL DEPARTMENTS

#url_to_open = "http://www.ninjacourses.com/explore/1/department/AEROSPC"
url_to_open = "http://www.ninjacourses.com/explore/1" 
file = file_open()
dept = raw_input("What department would you like to get info from? ")
soup = read_site(url_to_open + "/department/" + dept)
#dept_list_grab(soup, file)
course_info_grab(soup, file)
