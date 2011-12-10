from CategoryContainer import CategoryContainer, CategoryContainerError
from nose.tools import assert_raises

def add_new_category_test():
  c = CategoryContainer(2)
  c.addCategory("A", "testCategory")
  with assert_raises(CategoryContainerError):
    # Only one key shortcuts
    c.addCategory("AD", "asdsad")
  with assert_raises(CategoryContainerError):
  # No double shortcut assingment
    c.addCategory("A", "asdsad")

def remove_category_test():
  c = CategoryContainer(2)
  c.addCategory("A", "testCategory")
  c.removeCategory("A")

  assert c.listCategories() == {}

def change_category_test():
  c = CategoryContainer(2)
  c.addCategory("A", "testCategory")
  c.changeCategory("A", "B", "nothing")

  assert c.listCategories() == {"B":"nothing"}

def categorisation_test():
  c = CategoryContainer(2)
  assert_raises(CategoryContainerError, c.categorise, (1, "A"))
  c.addCategory("A", "a test category")
  c.categorise(1, "A")
  assert c.listCategorisations() == {1: "A", 2: None}

def name_of_shortcut_test():
  c = CategoryContainer(100)
  c.addCategory("E", "lalelu")
  assert c.nameOf("E") == "lalelu"

def next_not_categoriesed_index_test():
  c = CategoryContainer(2)
  c.addCategory("W", "sad")
  assert c.nextNotCategorisedIndex() == 1
  c.categorise(1, "W")
  assert c.nextNotCategorisedIndex() == 2
  c.categorise(2, "W")
  assert c.nextNotCategorisedIndex() == None

def change_category_with_categorisations_test():
  c = CategoryContainer(2)
  c.addCategory("A", "testCategory")
  c.categorise(1, "A")
  c.changeCategory("A", "B", "nothing")

  assert c.listCategorisations() == {1: "B", 2: None}
  
def remove_category_with_categorisations_test():
  c = CategoryContainer(2)
  c.addCategory("A", "testCategory")
  c.categorise(1, "A")
  c.removeCategory("A")
  
  assert c.listCategorisations() == {1: None, 2: None}
