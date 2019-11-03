# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
import sqlite3

class VideosVideoIdTag(Resource):

    def post(self, video_id):
        print(g.json)
        print(g.headers)

        for param in ["tag", "user_id"]:
            if param not in g.json:
                return {"errorMessage": f"param {param} not in body"}, 400

        # check tag is an existing tag for the user
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        SQL = f"SELECT * FROM tags where user_id=? and tag=?;"
        c.execute(SQL, (g.json["user_id"],g.json["tag"],))
        tags_entries = c.fetchall()
        conn.close()
        if len(tags_entries) == 0:
            print(f"tag {g.json['tag']} doesn't exist for user {g.json['user_id']}")
            return {"errorMessage": f"tag {g.json['tag']} doesn't exist for user {g.json['user_id']}"}, 400
        
        tag_id = tags_entries[0][0]
        #if video not created, create video with that tag
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        SQL = f"SELECT * FROM videos where id=?;"
        c.execute(SQL, (video_id,))
        videos_entries = c.fetchall()
        conn.close()
        if len(videos_entries) == 0:
            # create video
            SQL = f"INSERT INTO videos (id, user_id, video_title, categories) values (?,?,?,?)"
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            # TODO get video title from youtube api and category
            c.execute(
                SQL,
                (
                    video_id,
                    g.json["user_id"],
                    "GET VIDEO TITLE",
                    tag_id,
                ),
            )
            conn.commit()
            conn.close()
        else: # update the videos tag
            print(f"Updating {video_id} to {g.json['tag']}")
            SQL = f"UPDATE videos SET categories=? WHERE id=?;"
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute(SQL, (tag_id, video_id,))
            conn.commit()
            conn.close()
            

        print("successfuly set tag")
        return {"videos": {"video_id": 1}}, 200
        #return {"message": f"successfully set video to have category {g.json['tag']}"}, 200, None