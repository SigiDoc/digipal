from django.template import Library
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
import re

register = Library()

@stringfilter
def spacify(value, autoescape=None):
    if autoescape:
	esc = conditional_escape
    else:
	esc = lambda x: x
    return mark_safe(re.sub('\s', '%20', esc(value)))
spacify.needs_autoescape = True
register.filter(spacify)

@register.filter(is_safe=True)
@stringfilter
def anchorify(value):
    """
    Like slugify() but preserves the unicode chars
    The problem with slugify is that it will return an empty string for
    a single special char, or identical slugs for strings where only one
    special char varies.
    """
    #value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = re.sub(ur'(?u)[^\w\s-]', u'', value).strip()
    return mark_safe(re.sub(u'[-\s]+', u'-', value))

@register.filter(is_safe=True)
def update_query_strings(content, updates):
    '''
        Update the query strings found in an HTML fragment.
        
        E.g.
        
        >> update_query_string('href="http://www.mysite.com/path/?k1=v1&k2=v2" href="/home"', 'k2=&k5=v5')
        'href="http://www.mysite.com/path/?k1=v1&k5=v5" href="/home?k5=v5"'
        
    '''
    
    if len(content.strip()) == 0: return content
    
    # find all the URLs in content
    if '"' in content or "'" in content:
        # we assume the content is HTML
        parts = re.findall(ur'(?:src|href)="([^"]*?)"', content)
        parts += re.findall(ur"(?:src|href)='([^']*?)'", content)
    else:
        # we assume the content is a single URL
        parts = [content]
    
    # update all the urls found in content    
    for url in sorted(parts, key=lambda e: len(e), reverse=True):
        content = content.replace(url, update_query_string(url, updates))
        
    return content

def update_query_string(url, updates):
    '''
        Replace parameter values in the query string of the given URL.
        
        E.g.
        
        >> _update_query_string('http://www.mysite.com/about?category=staff&country=UK', 'who=bill&country=US')
        'http://www.mysite.com/about?category=staff&who=bill&country=US'

        >> _update_query_string('http://www.mysite.com/about?category=staff&country=UK', {'who': ['bill'], 'country': ['US']})
        'http://www.mysite.com/about?category=staff&who=bill&country=US'
    '''
    ret = url.strip()
    if ret and ret[0] == '#': return ret
    
    updates_dict = updates

    from urlparse import urlparse, urlunparse, parse_qs
    from urllib import urlencode
    
    # Convert string format into a dictionary
    if isinstance(updates, basestring):
        updates_dict = parse_qs(updates, True)
    
    parts = [p for p in urlparse(url)]
    query_dict = parse_qs(parts[4])
    query_dict.update(updates_dict)
    
    # Now query_dict is our updated query string as a dictionary 
    # Parse and unparse it again to remove the empty values
    query_dict = parse_qs(urlencode(query_dict, True))
    
    # Convert back into a string    
    parts[4] = urlencode(query_dict, True)
    
    # Place the query string back into the URL
    ret = urlunparse(parts)

    return ret
