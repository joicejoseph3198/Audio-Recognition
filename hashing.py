# import stuff
class Audio_Recognition():
    def __init__(self):
        self.anchor_delay = 3 
        self.target_zone = 5
        self.round_off = 6

    def hash_function(self,song,is_target):
        
        try:
            x = song.filtered
            print("Found filtered spectogram for", song.name," in database")
        except:
            # x = function_that_returns_filtered_Spectogram()
            # x has structure: {'time_slice':list_of_preserved_frequencies: e.g.: '1':[freq, freq2, etc.], '2':[freq1, freq2, etc.]}
            if not is_target:
                song.dump_in_the_database()

        time_res = song.time_res

        numbered_pts = {}
        i = 0 
        for time in sorted(x.keys()):
            for freq in sorted(x[time]):
                numbered_pts[i] = (time,freq)
                i+=1
        song.total_pts = i
    
        print("Total freq points in song", song.name, "are", song.total_pts)

        
        # database is a dictionary with: key = (anchor freq, point freq, delta time), value = (absolute time of anchor, song id)
        # couple is the above mentioned key-value pair
        total_couples = 0
        anchor = 0
        
        #if it is an audio file to be added to the database, we use song_name as song_id
        if not is_target: 
            # anchor point is the first point
            freq_anchor, time_anchor = numbered_pts[0][1], numbered_pts[0][0]

            for start in range(self.anchor_delay): 
                freq_pt, time_pt = numbered_pts[start][1], numbered_pts[start][0]
                cur_key = (freq_anchor, freq_pt,round((time_pt-time_anchor)*time_res,self.round_off))
                cur_val = (round(time_anchor*time_res, self.round_off), song.name)
                total_couples+=1
                
                if cur_key not in self.database.keys():
                    self.database[cur_key] = []
                self.database[cur_key].append(cur_val)

            #each point will act as an anchor for next 5 points in filtered spectogram
            for anchor in range(song.total_pts-self.target_zone-self.anchor_delay+1):
                freq_anchor, time_anchor = numbered_pts[anchor][1], numbered_pts[anchor][0]
                
				#target zone stretches from anchor_point+anchor_delay to anchor_point+anchor_delay+target_zone_suze
                for target_pt in range(anchor+self.anchor_delay, anchor+self.anchor_delay+self.target_zone):
                    freq_pt, time_pt = numbered_pts[target_pt][1], numbered_pts[target_pt][0]
                    cur_key = (freq_anchor, freq_pt, round((time_pt-time_anchor)*time_res, self.round_off))
                    cur_val = (round(time_anchor*time_res, self.round_off), song.name)
                    total_couples +=1 

                    if cur_key not in self.database.keys():
                        self.database[cur_key] = []
                    self.database[cur_key].append(cur_val)

            song.total_couples = total_couples
            print("Total couples for song",song.name,'are',total_couples)

        else:
            freq_anchor, time_anchor = numbered_pts[0][1], numbered_pts[0][0]

            to_return = {}
            total_couples = 0 

            for start in range(self.anchor_delay):
                freq_pt, time_pt = numbered_pts[start][1], numbered_pts[start][0]
                cur_key = (freq_anchor, freq_pt, round((time_pt-time_anchor)*time_res, self.round_off))
                cur_val = round(time_anchor*time_res, self.round_off)

                if cur_key not in to_return.keys():
                    to_return[cur_key] = []
                to_return[cur_key].append(cur_val)
                total_couples +=1 

            for anchor in range(song.total_pts-self.target_zone-self.anchor_delay+1):
                
                freq_anchor, time_anchor = numbered_pts[anchor][1], numbered_pts[anchor][0]
            
                for target_pt in range(anchor+self.anchor_delay, anchor+self.anchor_delay+self.target_zone):
                    freq_pt, time_pt = numbered_pts[target_pt][1], numbered_pts[target_pt][0]
                    cur_key = (freq_anchor, freq_pt, round((time_pt-time_anchor)*time_res, self.round_off))
                    cur_val = round(time_anchor*time_res, self.round_off)

                    if cur_key not in to_return.keys():
                        to_return[cur_key] = []
                    to_return[cur_key].append(cur_val)
                    total_couples +=1

            print("Total couples for song",song.name,'are',total_couples) 

            return to_return            

