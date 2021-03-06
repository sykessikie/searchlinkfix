result = None

def init_results():
  global result
  result = driver.find_element_by_partial_link_text("mini-profiler")
  return result

def assert_link_unchanged():
  global result, href
  assert result.get_attribute("href") == href

def assert_no_intermediate_urls(method, target):
  driver.get_urls()
  method()
  urls = []
  def check_urls():
    urls.extend(driver.get_urls())
    return urls
  driver.wait_until(check_urls)
  assert urls[0] == target

def close_windows(keep):
  for h in [h for h in driver.window_handles if h != keep]:
    driver.switch_to.window(h)
    driver.close()
  driver.switch_to.window(keep)

# Open Groups post
driver.get("https://groups.google.com/d/msg/play-framework/ZfmjuYnZrzg/2hx2zgq_GugJ")
driver.wait_until(init_results)

# Check link URL
href = result.get_attribute("href")
assert "google.com" not in href

# Right-click the link
driver.chain(lambda c: c.context_click(result))
assert_link_unchanged()
driver.chain(lambda c: c.send_keys(driver.keys.ESCAPE))
assert_link_unchanged()

# Click the link
orig_window = driver.current_window_handle
assert_no_intermediate_urls(lambda: result.click(), href)
close_windows(keep=orig_window)
assert_link_unchanged()

# Middle-click search result
assert_no_intermediate_urls(lambda: result.middle_click(), href)
driver.close_background_tabs()
assert_link_unchanged()

# Click Apps button to bring up dropdown
driver.find_element_by_css_selector("a[title='Apps']").click()
driver.wait_until(lambda: driver.find_element_by_css_selector("div[aria-label='Apps']"))
