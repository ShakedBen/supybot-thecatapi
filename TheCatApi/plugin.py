###
# Copyright (c) 2015, Andrew Phillips
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import re
import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('TheCatApi')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


class TheCatApi(callbacks.Plugin):
    """Provides access to http://thecatapi.com/"""
    pass

    threaded = True

    idRe = re.compile('^[a-zA-Z0-9]+$')

    xmlCatIdRe = re.compile('<id>([a-zA-Z0-9]+)</id>')
    xmlCatUrlRe = re.compile('<source_url>(.+)</source_url>')
    
    def _fetchXml(self, cmd, args):
        urlBase = self.registryValue('urlBase')
        api = self.registryValue('apiId')

        url = urlBase + cmd + '?format=xml'
        if api:
            url = url + '&api=%s' % api

        if len(args) != 0:
            url = url + '&' + '&'.join(args)

        #return url
        return utils.web.getUrl(url)

    def _formatCat(self, result):
        catId = 'Unknown'
        catIdMatches = self.xmlCatIdRe.search(result)
        if catIdMatches:
            catId = catIdMatches.group(1)
        
        catUrl = 'Unknown'
        catUrlMatches = self.xmlCatUrlRe.search(result)
        if catUrlMatches:
            catUrl = catUrlMatches.group(1)
            
        return 'Cat "%s": %s' % (catId, catUrl)

    def cat(self, irc, msg, args, catId):
        """[id]
        Returns cat matching [id] or a random cat.
        """

        result = ''
        if catId is '':
            result = self._fetchXml("/images/get", [])
        else:
            if self.idRe.match():
                result = self._fetchXml("/images/get", ['image_id=' + catId])

        irc.reply(self._formatCat(result))        
    cat = wrap(cat, [additional(('somethingWithoutSpaces', 'cat id'), '')])

    def catgif(self, irc, msg, args):
        """
        Returns a cat with a type of gif
        """

        result = self._fetchXml("/images/get", ['type=gif'])
        irc.reply(self._formatCat(result))        
    catgif = wrap(catgif)
Class = TheCatApi


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
