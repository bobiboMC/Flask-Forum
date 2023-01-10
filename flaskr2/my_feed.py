from feedgen.feed import FeedGenerator
fg = FeedGenerator()
fg.id('http://lernfunk.de/media/654321')
fg.title('Some Testfeed')
fg.author( {'name':'John Doe','email':'john@example.de'} )
fg.link( href='http://example.com', rel='alternate' )
fg.logo('http://ex.com/logo.jpg')
fg.subtitle('This is a cool feed!')
fg.link( href='http://larskiesow.de/test.atom', rel='self' )
fg.language('en')
print(fg.author())
fe = fg.add_entry()
fe.id('http://lernfunk.de/media/654321/1')
fe.title('The First Episode')
rssfeed  = fg.rss_str(pretty=True) # Get the RSS feed as string
fg.rss_file('rss.xml') # Write the RSS feed to a file
