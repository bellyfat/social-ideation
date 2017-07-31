import requests
import json

def doUpdateSessionkey(url, email, password):
    params =  {"email": email, "password": password}
    headers = {"content-type": "application/json; charset=utf8"}
    r = requests.post(url, headers=headers, json=params)
    if r.status_code == 200:
        response = r.json()
        return response["sessionKey"]
    else:
        return None

def doRequest(url, method="get", body=None, params=None, headers=None):
    if method == "get":
        if params == None:
            r = requests.get(url, headers=headers)
        else:
            r = requests.get(url, headers=headers, params=params)

    elif method == "post":
        r = requests.post(url, headers=headers, json=body)

    elif method == "put":
        if body == None:
            r = requests.put(url, headers=headers)
        else:
            r = requests.put(url, headers=headers, json=body)

    if r.status_code == 200:
        return r.json()
    else:
        r.raise_for_status()


class appcivist_api():
    base_url = ""
    session_key = ""

    ignore_admin_user =""
    social_ideation_source=""
    social_ideation_source_url=""
    social_ideation_user_source_url=""
    social_ideation_user_source_id=""

    def set_headers(self):
        headers = {"SESSION_KEY": self.session_key, "IGNORE_ADMIN_USER": self.ignore_admin_user, 
                  "SOCIAL_IDEATION_SOURCE": self.social_ideation_source, 
                  "SOCIAL_IDEATION_SOURCE_URL": self.social_ideation_source_url, 
                  "SOCIAL_IDEATION_USER_SOURC_ID": self.social_ideation_user_source_id, 
                  "SOCIAL_IDEATION_USER_SOURCE_URL": self.social_ideation_user_source_url}
        return headers


    # return list of all memebers of the assembly
    # GET /api/assembly/:id/membership/:status
    # implemented by using the get_all_authors method
    def get_users(self, aid):
        return self.get_all_authors(aid)


    # return info about a single member
    # GET /api/user/:uid 
    # GET /api/user/:uid/profile
    # implemented by using the get_author_detail method
    def get_user_details(self, uid):
        return self.get_author_info(uid)


    # tengo que diferenciar entre author y user despues
    # GET /api/assembly/:id/membership/:status
    # una vez que tenga los ids de los miembros debo llamar a get_author_detail
    # for each item in response, append item['user']
    def get_all_authors(self, aid):
        list_of_users = []
        url = self.base_url + "/api/assembly/" + str(aid) + "/membership/ACCEPTED"
        headers = {"SESSION_KEY": self.session_key}
        response = doRequest(url=url, method="get", headers=headers)
        for membership in response:
            list_of_users.append(membership["user"])
        return list_of_users


    # tengo que diferenciar entre author y user despues
    # GET /api/user/:uid (Get a user by id) (to check if user info is updated)
    # GET /api/user/:uid/profile   
    def get_author_info(self, uid):
        url = self.base_url + "/api/user/" + str(uid)
        headers = {"SESSION_KEY": self.session_key}
        response = doRequest(url=url, method="get", headers=headers)
        return response


    # return the list of capaigns of an assembly
    # GET /api/assembly/:aid/campaign (List campaigns of an Assembly)
    def get_campaigns(self, aid):
        url = self.base_url + "/api/assembly/" + str(aid) + "/campaign"
        headers = {"SESSION_KEY": self.session_key}
        response = doRequest(url=url, method="get", headers=headers)
        return response


    # return all the proposals
    # GET /api/assembly/:aid/campaign (List campaigns of an Assembly)
    # GET /api/assembly/:aid/campaign/:cid/contribution (Get contributions in a Campaign)
    def get_proposals_of_campaign(self, aid, cid):
        # url = self.base_url + "/api/assembly/" + str(aid) + "/contribution"
        url = self.base_url + "/api/assembly/" + str(aid) + "/campaign/" + str(cid) + "/contribution"
        headers = {"SESSION_KEY": self.session_key}
        params = {"type": "proposal"}
        response = doRequest(url=url, method="get", headers=headers, params=params)
        final_list = []
        for proposal in response:
            if "firstAuthor" in proposal.keys():
                final_list.append(proposal)
        return final_list


    # return info about a single proposal
    # GET /api/assembly/:aid/contribution/:cid
    def get_proposal_details(self, aid, coid):
        url = self.base_url + "/api/assembly/" + str(aid) + "/contribution/" + str(coid)
        headers = {"SESSION_KEY": self.session_key}
        response = doRequest(url=url, method="get", headers=headers)
        return response


    # return all proposals of an assembly
    # Implemented with get_campaigns() and get_proposals_of_campaign() methods
    def get_all_proposals(self, aid):
        list_of_proposals = []
        campaigns = self.get_campaigns(aid)
        for c in campaigns:
            proposals = self.get_proposals_of_campaign(aid, c["campaignId"])
            for p in proposals:
                list_of_proposals.append(p)
        return list_of_proposals        


    # return the list of comments of a proposal
    # GET /api/assembly/:aid/contribution/:cid/comment (no me sirve este. No retorna bien)
    # GET /api/space/:sid/contribution (1st, get the discussion, then, foreach discussion get comments)
    def get_comments_of_proposal(self, sid):
        list_of_comments = []
        url = self.base_url + "/api/space/" + str(sid) + "/contribution?type=DISCUSSION"
        headers = {"SESSION_KEY": self.session_key}
        response = doRequest(url=url, method="get", headers=headers)
        for item in response["list"]:
            list_of_comments.append(item)
            url = self.base_url + "/api/space/" + str(item["resourceSpaceId"]) + "/contribution?type=COMMENT"
            response2 = doRequest(url=url, method="get", headers=headers)
            for item2 in response2["list"]:
                list_of_comments.append(item2)
        return list_of_comments


    # return the list of comments of a campaign
    # GET /api/assembly/:aid/contribution  (DIDN'T WORK)
    # implemented by using the get_proposals and get_comment_proposal methods
    def get_comments_of_campaign(self, aid, cid):
        list_of_comments = []
        proposals = self.get_proposals_of_campaign(aid, cid)
        for p in proposals:
            p_comments = self.get_comments_of_proposal(p["resourceSpaceId"])
            list_of_comments = list_of_comments + p_comments
        return list_of_comments


    # return the list of all comments of an assembly
    # implemented using the get_campaigns() and get_comments_of_camapign() methods
    def get_all_comments(self, aid):
        list_of_comments = []
        campaigns = self.get_campaigns(aid)
        for c in campaigns:
            comments = self.get_comments_of_campaign(aid, c["campaignId"])
            for co in comments:
                list_of_comments.append(co)
        return list_of_comments


    # return info about a single comment
    # GET /api/assembly/:aid/contribution/:cid
    def get_comment_details(self, aid, coid):
        url = self.base_url + "/api/assembly/" + str(aid) + "/contribution/" + str(coid)
        headers = {"SESSION_KEY": self.session_key}
        response = doRequest(url=url, method="get", headers=headers)
        return response


    # return the votes (called feedbacks on appcivist) of a single contribution
    # GET /api/assembly/:aid/contribution/:coid/feedback   
    # GET /api/assembly/:aid/campaign/:cid/contribution/:coid/feedback (It works with both endpoints)
    def get_feedbacks_of_contribution(self, aid, coid):
        url =  self.base_url + "/api/assembly/" + str(aid) + "/contribution/" + str(coid) + "/feedback"
        headers = {"SESSION_KEY": self.session_key}
        response = doRequest(url=url, method="get", headers=headers)
        return response

  
    # return the votes (called feedbacks on appcivist) of a single proposal
    def get_feedbacks_of_proposal(self, aid, coid):
        return self.get_feedbacks_of_contribution(aid, coid)


    # return the votes (called feedbacks on appcivist) of a single comment
    # implemented by using the get_feedback_proposal method since 
    # the endpoint is for appcivist's contributions in general (proposals and comments)
    def get_feedbacks_of_comment(self, aid, coid):
        return self.get_feedbacks_of_contribution(aid, coid)
    

    # return all the votes of all proposals of all campaigns
    # implemented tiwh get_campaigns(), get_proposals_of_campaign() and get_feedbacks_of_proposal() methods
    def get_feedbacks_of_all_proposals(self, aid):
        list_of_feedbacks = []
        campaigns = self.get_campaigns(aid)
        for c in campaigns:
            proposals = self.get_proposals_of_campaign(aid, c["campaignId"])
            for p in proposals:
                feedbacks = self.get_feedbacks_of_proposal(aid, p["contributionId"])
                list_of_feedbacks = list_of_feedbacks + feedbacks
        return list_of_feedbacks


    # return all the votes of all comments of all campaigns
    # implemented with get_campaigns(), get_comments_of_campaign() and get_feedbacks_of_comment() methods
    def get_feedbacks_of_all_comments(self, aid):
        list_of_feedbacks = []
        campaigns = self.get_campaigns(aid)
        for c in campaigns:
            comments = self.get_comments_of_campaign(aid, c["campaignId"])
            for c in comments:
                feedbacks = self.get_feedbacks_of_comment(aid, c["contributionId"])
                list_of_feedbacks = list_of_feedbacks + feedbacks
        return list_of_feedbacks



    ###### POST METHODS
    # creates a new contribution
    # POST /api/space/:sid/contribution
    def create_proposal(self, sid, proposal):
        url = self.base_url + "/api/space/" + str(sid) + "/contribution"
        headers = self.set_headers()
        response = doRequest(url=url, method="post", headers=headers, body=proposal)
        return response


    # creates a comment (appcivist's DICUSSION) on an proposal
    # implemented with create_proposal() method since it uses the same contribution creation endpoint
    def comment_proposal(self, sid, discussion):
        return self.create_proposal(sid, discussion)


    # creates a comment on a Discussion
    # implemented with create_proposal() method since it uses the same contribution creation endpoint
    def comment_discussion(self, sid, comment):
        return self.create_proposal(sid, comment)


    ###### PUT METHODS
    # Add a positive feedback ("vote up") a proposal
    # PUT /api/assembly/:aid/campaign/:caid/contribution/:cid/feedback
    def vote_up_proposal(self, aid, caid, coid):
        url = self.base_url + "/api/assembly/" + str(aid) + "/campaign/" + str(caid) \
              + "/contribution/" + str(coid) + "/feedback"
        headers = self.set_headers()
        test_body = {"up": "true", "down": "false", "fav": "false", "flag": "false",
                     "type": "MEMBER", "status": "PUBLIC"}
        response = doRequest(url=url, method="put", headers=headers, body=test_body)
        return response


    # Add a negative feedback, ("vote down") a proposal
    # PUT /api/assembly/:aid/campaign/:caid/contribution/:cid/feedback
    def vote_down_proposal(self, aid, caid, coid):
        url = self.base_url + "/api/assembly/" + str(aid) + "/campaign/" + str(caid) \
              + "/contribution/" + str(coid) + "/feedback"
        headers = self.set_headers()
        test_body = {"up": "false", "down": "true", "fav": "false", "flag": "false", 
                     "type": "MEMBER", "status": "PUBLIC"}
        response = doRequest(url=url, method="put", headers=headers, body=test_body)
        return response


    # Add a positive feedback ("vote up") a comment
    # Implemented with vote_up_proposal() method since both cases use the same Appcivist endpoint
    def vote_up_comment(self, aid, caid, coid):
        return self.vote_up_proposal(aid, caid, coid)


    # Add a negative feedback ("vote down") a comment
    # Implemented with vote_down_proposal() method since both cases use the same Appcivist endpoint
    def vote_down_comment(self, aid, caid, coid):
        return self.vote_down_proposal(aid, caid, coid)


    ##### DELETE METHODS
    # Deletes a contribution. General methods used to implemente delete_proposal() and delete_comment()
    # PUT       /api/assembly/:aid/contribution/:cid/softremoval
    # The request is a PUT request since appcivist's endpoint do an soft-removal (data is marked as removed,
    # but it is not actually delete from the database)
    def delete_contribution(self, aid, coid):
        url = self.base_url + "/api/assembly/" + str(aid) + "/contribution/" + str(coid) + "/softremoval"
        headers = self.set_headers()
        response = doRequest(url=url, method="put", headers=headers)
        return response


    # Deletes a proposal
    # implementented with detele_contribution() method
    def delete_proposal(self, aid, coid):
        return delete_contribution(aid, coid)


    # Deletes a comment
    # implemented with delete_contribution() method
    def delete_comment(self, aid, coid):
        return delete_contribution(aid, coid)