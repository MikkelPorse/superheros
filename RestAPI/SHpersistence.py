from tinydb import TinyDB

class SuperHeroStore(object):
    """
    A persistence abstraction layer with basic CRUD functionality

    usage:
    from SHpersistence import SuperHeroStore
    store = SuperHeroStore('/path/to/yourdbfile.json')
    """

    def __init__(self,path):
        """
        Instantiate with path to your database file (.json)
        """
        self.dbpath = path
        
    def create_hero(self, heroname, herodata, dc_or_marvel = 'dc'):
        """
        Creates a hero entry
        
        heroname -- name of the hero
        herodata -- the text describing the hero (wikipedia article)
        dc_or_marvel -- indicator of which comic universe the hero belongs to 
        """
        assert heroname is not None, 'Please specify heroname'
        assert herodata is not None, 'Please specify herodata'
        assert dc_or_marvel in ['dc','marvel'], "Please specify 'dc' or 'marvel' only"
        
        with TinyDB(self.dbpath) as db:
            return db.insert({'name':heroname, 'text':herodata,'dc_or_marvel':dc_or_marvel})
   
    def read_hero(self, id):
        """
        Reads a hero from the database. Returns json
        """
        assert id is not None, 'Please specify id'
        
        with TinyDB(self.dbpath) as db:
            hero = db.get(eid=int(id))
            return hero
            # return {'id': id, 'name':hero['name'], 'herodata': hero['text'], 'dc_or_marvel':hero['dc_or_marvel']}
        
    def update_hero(self, id, heroname, herodata, dc_or_marvel):
        """
        updates a hero entry
        
        heroname -- the key to update
        herodata -- the text describing the hero (wikipedia article)
        dc_or_marvel -- indicator of which comic universe the hero belongs to
        """
    
        assert heroname is not None, 'Please specify heroname'
        assert herodata is not None, 'Please specify herodata'
        assert dc_or_marvel in ['dc','marvel'], "Please specify 'dc' or 'marvel' only"

        with TinyDB(self.dbpath) as db:
            db.update({'name':heroname, 'text':herodata, 'dc_or_marvel':dc_or_marvel },eids=[id])
   
    def delete_hero(self, id):
        """Delete a hero from database"""
        
        assert id is not None, 'Please specify heroname'
        with TinyDB(self.dbpath) as db:
            db.remove(eids =[id])

    def hero_exists(self, id):
        with TinyDB(self.dbpath) as db:
            return db.contains(eids=[int(id)])

    def list_heros(self):
        with TinyDB(self.dbpath) as db:
            return [{'id':el.eid,'name':el['name'],'dc_or_marvel': el['dc_or_marvel']} for el in db.all()]

    def get_everything(self):
        with TinyDB(self.dbpath) as db:
            return db.all()

    def nuke_everything(self):
        """ Just as it says."""
        with TinyDB(self.dbpath) as db:
            db.purge()
        

if __name__ == '__main__':
    """ A quick little testharness  """
    s = SuperHeroStore('test.json')
    s.nuke_everything()
    
    print 'writing hulk to test.json'
    id = s.create_hero('hulk','Bruce Banner getting green...', 'marvel')
    print id
    
    print 'read hulk from test.json'
    print s.read_hero(id)
    
    print s.list_heros()
    
    print 'update hulk in test.json'
    s.update_hero(id, 'hulk','Bruce Banner got green!', 'marvel')
    print s.read_hero(id)
    
    s.delete_hero(id), 
    print s.read_hero(id)
    s.nuke_everything()    