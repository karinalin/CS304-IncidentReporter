import sys
import MySQLdb

ADDED_BY = 1341
    
def getConn(db):
    conn = MySQLdb.connect(host='localhost',
                           user='ubuntu',
                           passwd='',
                           db=db)
    return conn
    
def getUserInformation(conn, userID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    try:
        curs.execute('''select * from user where userID = %s''', [userID])
        return curs.fetchone()
    except:
        return None
        
def getAllMovies(conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    try: 
        curs.execute('''select movie.tt as tt, movie.title as title, movie.`release` as `release`, 
        movie.director as director, movie.addedby as addedby, movie.avg_rating as average, 
        person.name as directorName from movie 
        left join person on movie.director = person.nm''') 
        return curs.fetchall()
    except: # Handle duplicate entries where tt already exist
        return False
        

        
def calculateAverage(conn, tt):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    
    try:
        curs.execute('''UPDATE movie SET movie.avg_rating = (SELECT AVG(rating) 
        from rating where rating.tt= %s) WHERE movie.tt = %s;''', [tt, tt])
        conn.commit()
        
        curs.execute('''SELECT avg_rating from movie where tt = %s''', [tt])
        
        return curs.fetchone()
    except:  
        return False

def getMovieByTitle(conn, title):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    try:
        curs.execute('''select movie.tt as tt, movie.title as title, movie.`release` as `release`, 
        movie.director as director, movie.addedby as addedby, movie.avg_rating as average, 
        person.name as directorName from movie 
        left join person on movie.director = person.nm where title REGEXP %s''', [title]) 
        return curs.fetchall()
    except:
        return None
            
        
def updateUserRating(conn, uid, tt, rating):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select * from rating where tt=%s and uid= %s''', [tt, uid])
    updateRating = curs.fetchone()
        
    if updateRating:
        try:
            curs.execute('''UPDATE rating
                        SET rating = %s
                        WHERE tt=%s and uid = %s''', [rating, tt, uid])
            conn.commit()
            return True
        except:  
            return False
    else:
        try:
            curs.execute('''INSERT INTO rating
                        (uid, tt, rating)
                        VALUES (%s, %s, %s)''', [uid,tt,rating])
            conn.commit()
            return True
        except:  
            return False

        
if __name__ == '__main__':
    conn = getConn('wmdb')
    print(updateUserRating(conn, 12, 666, 4))
    print(updateUserRating(conn, 14, 666, 5))
    print(updateUserRating(conn, 14, 666, 3))
    print(calculateAverage(conn, 666))
    
