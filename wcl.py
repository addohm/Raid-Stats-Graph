from decouple import config

class WCL():
    """
    A class used to retrieve WarcraftLogs data

    Attributes
    ----------
    request_uri : str
        The URI requests will be made from

    api_key : str
        The secret key used in the URI requests

    Methods
    -------
    get_zone_list()
        Gets an array of Zone objects. Each zone corresponds to a raid/dungeon instance in the game and has its own set of encounters.
    get_class_list()
        Gets an array of Class objects. Each Class corresponds to a class in the game.
    get_rankings_list_encounter(encounterID, params)
        Gets an object that contains a total count and an array of EncounterRanking objects and a total number of rankings for that encounter. Each EncounterRanking corresponds to a single character or guild/team.
    get_rankings_list_character(characterName, serverName, serverRegion, params)
        Gets an array of CharacterRanking objects. Each CharacterRanking corresponds to a single rank on a fight for the specified character.
    get_parses_list_character(characterName, serverName, serverRegion, params)
        Obtains all parses for a character in the zone across all specs. Every parse is included and not just rankings.
    get_reports_list_guild(guildName, serverName, serverRegion, params)
        Gets an array of Report objects. Each Report corresponds to a single calendar report for the specified guild.
    get_reports_list_user(userName, params)
        Gets an array of Report objects. Each Report corresponds to a single calendar report for the specified user's personal logs.
    get_report_list_encounter(code, params)
        Gets arrays of fights and the participants in those fights. Each Fight corresponds to a single pull of a boss.
    get_report_list_events(view, code, params)
        Gets a set of events based off the view you're asking for. This exactly corresponds to the Events view on the site.
    get_report_list_tables(view, code, params)
        Gets a table of entries, either by actor or ability, of damage, healing and cast totals for each entry. This API exactly follows what is returned for the Tables panes on the site. It can and will change as the needs of those panes do, and as such should never be considered a frozen API. Use at your own risk.
    """
    from datetime import datetime, timedelta, timezone
    request_uri = 'https://classic.warcraftlogs.com:443/v1'
    api_key = config('API_KEY')

    def __make_request(self, uri):
        '''Makes GET request using the formatted URI
        Parameters
        ----------
        uri : str
            A fully qualified URI.

        Raises
        ------
        '''
        import requests
        response = requests.get(uri)
        return response.json()

    def __format_params(self, params):
        '''Formats a dictionary of parameters to be used in the URI
        Parameters
        ----------
        params : dict
            A dictionary of parameters and their values.
            ex: {'param1':'value','param2':'value', ...}

        Raises
        ------
        '''
        paramstring = ''
        for key, value in params.items():
            paramstring = paramstring + '&' + key + '=' + str(value)
        return paramstring[1:]

    def get_zone_list(self):
        '''Gets an array of Zone objects. Each zone corresponds to a raid/dungeon instance in the game and has its own set of encounters.
        https://classic.warcraftlogs.com/v1/docs/#!/Zones/zones_get'''
        uri = f'{self.request_uri}/zones&api_key={self.api_key}'
        return self.__make_request(uri)

    def get_class_list(self):
        '''Gets an array of Class objects. Each Class corresponds to a class in the game.
        https://classic.warcraftlogs.com/v1/docs/#!/Classes/classes_get'''
        uri = f'{self.request_uri}/classes&api_key={self.api_key}'
        return self.__make_request(uri)

    def get_rankings_list_encounter(self, encounterID, params={}):
        '''Gets an object that contains a total count and an array of EncounterRanking objects and a total number of rankings for that encounter. Each EncounterRanking corresponds to a single character or guild/team.
        https://classic.warcraftlogs.com/v1/docs/#!/Rankings
                
        Parameters
        ----------
        sound : str, optional
            The sound the animal makes (default is None)
            Currently available: metric, size, difficulty, partition, class, spec, bracket, server, region, page, filter

        Raises
        ------
        '''
        uri = f'{self.request_uri}/rankings/encounter/{encounterID}?{self.__format_params(params)}&api_key={self.api_key}'
        return self.__make_request(uri)

    def get_rankings_list_character(self, characterName, serverName, serverRegion, params={}):
        '''Gets an array of CharacterRanking objects. Each CharacterRanking corresponds to a single rank on a fight for the specified character.
        https://classic.warcraftlogs.com/v1/docs/#!/Rankings/rankings_character_characterName_serverName_serverRegion_get
                
        Parameters
        ----------
        characterName : str
            The name of the character to collect rankings for.

        serverName : slug str
            The server that the character is found on. For World of Warcraft this is the 'slug' field returned from their realm status API.

        serverRegion : str
            The short region name for the server on which the character is located: US, EU, KR, TW, CN.

        params : dict
            A dictionary of additional URI parameters
            Currently available: zone, encounter, metric, bracket, partition, timeframe

        Raises
        ------
        '''
        uri = f'{self.request_uri}/rankings/character/{characterName}/{serverName}/{serverRegion}?{self.__format_params(params)}&api_key={self.api_key}'
        return self.__make_request(uri)

    def get_parses_list_character(self, characterName, serverName, serverRegion, params={}):
        '''Obtains all parses for a character in the zone across all specs. Every parse is included and not just rankings.
        https://classic.warcraftlogs.com/v1/docs/#!/Parses/parses_character_characterName_serverName_serverRegion_get
                
        Parameters
        ----------
        characterName : str
            The name of the character to collect rankings for.

        serverName : slug str
            The server that the character is found on. For World of Warcraft this is the 'slug' field returned from their realm status API.

        serverRegion : str
            The short region name for the server on which the character is located: US, EU, KR, TW, CN.

        params : dict
            A dictionary of additional URI parameters
            Currently available: zone, encounter, metric, bracket, compare, partition, timeframe
        
        Raises
        ------
        '''
        uri = f'{self.request_uri}/parses/character/{characterName}/{serverName}/{serverRegion}?{self.__format_params(params)}&api_key={self.api_key}'
        return self.__make_request(uri)

    def get_reports_list_guild(self, guildName, serverName, serverRegion, params={}):
        '''Gets an array of Report objects. Each Report corresponds to a single calendar report for the specified guild.
        https://classic.warcraftlogs.com/v1/docs/#!/Reports/reports_guild_guildName_serverName_serverRegion_get
                
        Parameters
        ----------
        guildName : str
            The name of the guild to collect reports for.

        serverName : slug str
            The server that the character is found on. For World of Warcraft this is the 'slug' field returned from their realm status API.

        serverRegion : str
            The short region name for the server on which the character is located: US, EU, KR, TW, CN.

        params : dict
            A dictionary of additional URI parameters
            Currently available: start, end

        Raises
        ------
        '''
        uri = f'{self.request_uri}/reports/guild/{guildName}/{serverName}/{serverRegion}?{self.__format_params(params)}&api_key={self.api_key}'
        return self.__make_request(uri)

    def get_reports_list_user(self, userName, params={}):
        '''Gets an array of Report objects. Each Report corresponds to a single calendar report for the specified user's personal logs.
        https://classic.warcraftlogs.com/v1/docs/#!/Reports/reports_user_userName_get
                
        Parameters
        ----------
        userName : str
            The name of the user to collect reports for.

        params : dict
            A dictionary of additional URI parameters
            Currently available: start, end

        Raises
        ------
        '''
        uri = f'{self.request_uri}/reports/user/{userName}?{self.__format_params(params)}&api_key={self.api_key}'
        return self.__make_request(uri)

    def get_report_list_encounter(self, code, params={}):
        '''Gets arrays of fights and the participants in those fights. Each Fight corresponds to a single pull of a boss.
        https://classic.warcraftlogs.com/v1/docs/#!/Report/report_fights_code_get
                
        Parameters
        ----------
        code : str
            The specific report to collect fights and participants for.

        params : dict
            A dictionary of additional URI parameters
            Currently available: translate

        Raises
        ------
        '''
        uri = f'{self.request_uri}/report/fights/{code}?{self.__format_params(params)}&api_key={self.api_key}'
        return self.__make_request(uri)

    def get_report_list_events(self, view, code, params={}):
        '''Gets a set of events based off the view you're asking for. This exactly corresponds to the Events view on the site.
        https://classic.warcraftlogs.com/v1/docs/#!/Report/report_events_view_code_get
                
        Parameters
        ----------
        view : str
            The type of data requested. Supported values are 'summary', 'damage-done', 'damage-taken', 'healing', 'casts', 'summons', 'buffs', 'debuffs', 'deaths', 'threat', 'resources', 'interrupts' and 'dispels'.

        code : str
            The specific report to collect fights and participants for.

        params : dict
            A dictionary of additional URI parameters
            Currently available: start, end, hostility, sourceid, sourceinstance, sourceclass, targetid, targetinstance, targetclass, abilityid, death, options, cutoff, encounter, wipes, difficulty, filter, translate

        Raises
        ------
        '''
        uri = f'{self.request_uri}/report/events/{view}/{code}?{self.__format_params(params)}&api_key={self.api_key}'
        return self.__make_request(uri)

    def get_report_list_tables(self, view, code, params={}):
        '''Gets a table of entries, either by actor or ability, of damage, healing and cast totals for each entry. This API exactly follows what is returned for the Tables panes on the site. It can and will change as the needs of those panes do, and as such should never be considered a frozen API. Use at your own risk.
        https://classic.warcraftlogs.com/v1/docs/#!/Report/report_tables_view_code_get
                
        Parameters
        ----------
        view : str
            The type of data requested. Supported values are 'summary', 'damage-done', 'damage-taken', 'healing', 'casts', 'summons', 'buffs', 'debuffs', 'deaths', 'threat', 'resources', 'interrupts' and 'dispels'.

        code : str
            The specific report to collect fights and participants for.

        params : dict
            A dictionary of additional URI parameters.
            Currently available: start, end, hostility, by, sourceif, sourceinstance, sourceclass, targetid, targetinstance, targetclass, abilityid, options, cutoff, encounter, wipes, difficulty, filter, translate

        Raises

        ------
        '''
        uri = f'{self.request_uri}/report/tables/{view}/{code}?{self.__format_params(params)}&api_key={self.api_key}'
        return self.__make_request(uri)

if __name__ == "__main__":
    wcl = WCL()
    # test = wcl.get_rankings_list_encounter(611, {'metric':'dps','class':11})
    # test = wcl.get_rankings_list_character(characterName='Kampf', serverName='herod', serverRegion='US', params={'metric':'dps'})
    # https://classic.warcraftlogs.com:443/v1/reports/guild/not%20like%20this/herod/US?start=1234&end=5678&api_key=0325c4b75c2692c416959471a79bba51
    # https://classic.warcraftlogs.com:443/v1/reports/guild/not%20like%20this/herod/US?start=1234&end=5678&api_key=0325c4b75c2692c416959471a79bba51
    test = wcl.get_reports_list_guild('not like this', 'herod', 'US')
    print(test)



'''
    dateRange = 7 # days of data to pull

    class_id = {
        'Death Knight': 1,
        'Druid': 2,
        'Hunter': 3,
        'Mage': 4,
        'Monk': 5,
        'Paladin': 6,
        'Priest': 7,
        'Rogue': 8,
        'Shaman': 9,
        'Warlock': 10,
        'Warrior': 11,
        'Demon Hunter': 12,
    }
    encounterID = 0
    characterName = 'kampf'
    serverName = 'Herod'
    serverRegion = 'US'
    guildName = 'not like this'
    code = ''
    view = ''

    nowdate = datetime.now(tz=timezone.utc)
    startdate = nowdate - timedelta(days=dateRange)
    startdateUnix = int(startdate.timestamp() * 1000)
'''