from bs4 import BeautifulSoup
import urllib2
import os
import re
import sys, getopt

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
  
  instr_ratings = instr_ratings_grab(soup) # Is this even necessary??
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
  #li = li[5:]
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
  #depts = soup.find_all('li')[5:] # INCLUDES AC/HONOR/RC
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

def file_open(file_name):
  """ Define a file to be written to. Then, all contents needed will be
  placed in the file. 
  """
  ### Input file name to write to.
  file = open(file_name, 'a')
  return file

def file_write(file, course_name, course_desc, course_ratings):
  # Comment out only when using ALL DEPARTMENTS
  # file.write("Course Name, Course Desc, Num of Ratings, Overall Rating, Prof Name, Prof Rating\n")
  file.write("Course Name - Course Desc, OverallRating[Num of Ratings], Prof Name, Prof Rating")
  file.write("***--------------------****\n")
  file.write("\n")
  for x in range(len(course_name)):
    content = course_name[x] + " " + course_desc[x] + " " + course_ratings[x][0]
    file.write(content + '\n\n')
  file.close() #COMMENT OUT ONLY WHEN USING ALL DEPARTMENTS

def pick_uc(uc):
  if (uc == "Berkeley"):
    return str(1)
  if (uc == "Merced"):
    return str(2)
  if (uc == "Davis"):
    return str(3)
  if (uc == "Santa Barbara"):
    return str(4)
  if (uc == "LA"):
    return str(5)

def main(argv):
  ninja = "http://www.ninjacourses.com/explore/"
  uc = argv[0]
  uc = pick_uc(uc)
  dept = argv[1]
  url_to_open = ninja + uc + "/department/" 
  file = file_open(argv[2])
  soup = read_site(url_to_open + dept)
  course_info_grab(soup, file)

if __name__ == "__main__":
  main(sys.argv[1:])

