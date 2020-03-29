"""
File name: wizard.py
All the wizard functions for app.py
"""

@app.route("/competitions_wizard", methods=['GET', 'POST'])
def competitions_wizard():
    if 'username' in session:
        return "NOT now"
        # Note that we are not calling this function plain "random()" because random
        # is the name of a package we imported.
        # Step 1, Create a comp

        if "step" not in request.form:
            """
            Doesn't take anything
            Sends a page where users can send the application back a new comp data.
            """
            debugMessage("Redirect #1278313")
            return render_template("wizard.html", step="PAGE_CREATE_COMP")
        elif request.form["step"] == "PAGE_2":
            """
            When it's PAGE_2, it gets:
            UNAME, TEAMS, WIN_VMS, UNIX_VMS.

            It redirects it to PAGE_3.
            """
            try:
                error_message = ""

                UNAME = pymysql.escape_string(str(request.form['UNAME']))
                TEAMS = pymysql.escape_string(str(request.form['TEAMS']))

                # If some of them is empty.
                if (len(UNAME) < 1 or len(TEAMS) < 1):
                    pass

                WIN_VMS = pymysql.escape_string(request.values.get('WIN_VMS'))
                if len(WIN_VMS) < 1:
                    if debug:
                        error_message = "Missing WIN_VMS"
                        debugMessage(error_message)
                    return render_template('error.html', message= error_message ,url=url_for('competitions_team'),
                                           templates_length=getTemplatesLength(), tasks_length=getEventsLength())

                UNIX_VMS = pymysql.escape_string(request.values.get('UNIX_VMS'))
                if len(UNIX_VMS) < 1:
                    if debug:
                        error_message = "Missing UNIX_VMS"
                        debugMessage(error_message)
                    return render_template('error.html', message=error_message, url=url_for('competitions_team'),
                                           templates_length=getTemplatesLength(), tasks_length=getEventsLength())

                TOTAL_VMS = str(int(WIN_VMS) + int(UNIX_VMS))
                CREATED_FLAG = CREATED_FLAG_C = CREATED_TEAMS = TOTAL_CREATED_VMS = "0"

                # Create a COMPETITION
                raw_competitions_add(UNAME, TEAMS, CREATED_TEAMS, WIN_VMS, UNIX_VMS, TOTAL_VMS, TOTAL_CREATED_VMS,
                                     CREATED_FLAG, CREATED_FLAG_C)

                # Add teams objects to mysql so we use get_competition_teams(COMPETITION_NAME) in step "PAGE_3_PICK"
                for i in range(int(TEAMS)):
                    TEAM_tmp = "Team_" + str(i + 1)
                    raw_competitions_team_add(UNAME,
                                              TEAM_tmp,
                                              "0",
                                              "0",
                                              "0",
                                              "0",
                                              "0",
                                              "0",
                                              "0")

                # Move to the next page which is editing teams in step 2 template
                TEAMS = get_competition_teams(UNAME)
                debugMessage("Redirect #813613")
                return render_template("wizard.html", step="PAGE_3_PICK", UNAME=UNAME, TEAMS=TEAMS)
            except Exception as ex:
                if debug:
                    debugMessage("Couldn't create a comp")
                    debugMessage("Error: " + str(ex))
                    debugMessage("Block #134233")
        # Step 3, where we can create teams
        elif request.form["step"] == "PAGE_CREATE_TEAM":
            """
            PAGE_CREATE_TEAM, it helps creating teams using UNAME.

            """
            try:
                """
                This block tris to get some parameters that step "PAGE_3_PICK" should submit.
                If it didn't get all the parameters that means something went wrong, thus redirect to step "PAGE_3_PICK"
                """
                # Sanitize
                COMPETITION_NAME = UNAME = pymysql.escape_string(str(request.form['UNAME']))
                TEAM = pymysql.escape_string(str(request.form['TEAM']))

                # Get all elements of a comp
                # elements = get_all_elements_comp(UNAME)
                # debugMessage("Getting all elements: "+str(elements))
                # TEAMS = elements[2]
                # CREATED_TEAMS = elements[3]
                # if debug:
                #     debugMessage("Comparing "+str(TEAMS)+" and "+str(CREATED_TEAMS))
                #     debugMessage("Checking if we need more teams, TEAMS:" + str(TEAMS) + " > CREATED_TEAMS:" + str(
                #         CREATED_TEAMS) + " ?")
                # # Check if we need to create a new team.
                # if int(TEAMS) > int(CREATED_TEAMS):
                #     debugMessage("Redirect #841611")
                #     # Send it back to itself.
                return render_template("wizard.html", step="PAGE_CREATE_TEAM", UNAME=UNAME, TEAM=TEAM)
            except Exception as e:
                if debug:
                    debugMessage(e)
                    debugMessage("Error #72521 ")
                    debugMessage("Block #77823")

        elif request.form["step"] == "TAKE_PARAMETERS":
            """
            This block gets the values coming from PAGE_CREATE_TEAM and process it.
            Then redirect back to PAGE_3_PICK
            """
            try:
                COMPETITION_NAME = UNAME = pymysql.escape_string(str(request.form['UNAME']))
                TEAM = pymysql.escape_string(request.values.get('TEAM'))

                if len(TEAM) < 1:
                    if debug:
                        error_message = "Missing TEAM"
                        debugMessage(error_message)
                    return render_template('error.html', message=error_message, url=url_for('competitions_team'),
                                           templates_length=getTemplatesLength(), tasks_length=getEventsLength())

                DOMAIN_NAME = pymysql.escape_string(request.values.get('DOMAIN_NAME'))
                if len(DOMAIN_NAME) < 1:
                    if debug:
                        error_message = "Missing DOMAIN_NAME"
                        debugMessage(error_message)
                    DOMAIN_NAME = TEAM + ".com"

                SUBNET = pymysql.escape_string(request.values.get('SUBNET'))
                if len(SUBNET) < 1:
                    if debug:
                        error_message = "Missing SUBNET"
                        debugMessage(error_message)
                    return render_template('error.html', message=error_message, url=url_for('competitions_team'),
                                           templates_length=getTemplatesLength(), tasks_length=getEventsLength())

                GATEWAY = pymysql.escape_string(request.values.get('GATEWAY'))
                if len(GATEWAY) < 1:
                    if debug:
                        error_message = "Missing GATEWAY"
                        debugMessage(error_message)
                    return render_template('error.html', message=error_message, url=url_for('competitions_team'),
                                           templates_length=getTemplatesLength(), tasks_length=getEventsLength())

                DNS_SERVER1 = pymysql.escape_string(request.values.get('DNS_SERVER1'))
                if len(DNS_SERVER1) < 1:
                    if debug:
                        error_message = "Missing DNS_SERVER1"
                        debugMessage(error_message)
                    return render_template('error.html', message=error_message, url=url_for('competitions_team'),
                                           templates_length=getTemplatesLength(), tasks_length=getEventsLength())

                NIC = pymysql.escape_string(request.values.get('NIC'))
                if len(NIC) < 1:
                    if debug:
                        error_message = "Missing NIC"
                        debugMessage(error_message)
                    return render_template('error.html', message=error_message, url=url_for('competitions_team'),
                                           templates_length=getTemplatesLength(), tasks_length=getEventsLength())

                CREATED_FLAG = CREATED_VMS_FLAG = CONFIGURED_VMS_FLAG = "0"
                CREATED_FLAG_C = "1"  # So the team object knows that it has been edited

                """
                Since the team has been created in the past step we need to edit this.
                Edit a team and make an event.
                """
                safe_competitions_team_edit_by_name(COMPETITION_NAME,
                                                    TEAM,
                                                    DOMAIN_NAME,
                                                    SUBNET,
                                                    GATEWAY,
                                                    DNS_SERVER1,
                                                    NIC,
                                                    CREATED_FLAG,
                                                    CREATED_FLAG_C,
                                                    CREATED_VMS_FLAG,
                                                    CONFIGURED_VMS_FLAG)

                # Update
                update_CREATED_TEAMS_comp(COMPETITION_NAME)

                """
                In this stage they are two ways it can end up with.
                one - we still have teams to create.
                    How to go with that
                        Get the comp teams and created_teams and according to that move.

                    What it will happen
                        Goes back to PAGE_3_PICK
                Two - we don't have teams to create
                    How to go with that

                    What it will happen
                        move forward to step "PAGE_3_PICK_VMS"

                """

                elements = get_all_elements_comp(UNAME)
                TEAMS = elements[2]
                CREATED_TEAMS = elements[3]
                WIN_VMS = elements[4]
                UNIX_VMS = elements[5]
                TOTAL_VMS = elements[6]
                TOTAL_CREATED_VMS = elements[7]

                if int(TEAMS) > int(CREATED_TEAMS):
                    debugMessage("Redirect #841611")
                    # Send it back to pick another team to create/edit.
                    TEAMS = get_competition_teams(UNAME)
                    return render_template("wizard.html", step="PAGE_3_PICK", UNAME=UNAME, TEAMS=TEAMS)
                else:
                    """
                    At this point we need to start creating VMs for each team.
                    """
                    debugMessage("Redirect #198181")
                    # Get all teams
                    # Check if any team has no VMS
                    teams = next_unedited_vm(COMPETITION_NAME)
                    i = 0
                    for team in teams:
                        """
                        ID INTEGER NOT NULL AUTO_INCREMENT,
                        COMPETITION_NAME VARCHAR(50) NOT NULL,  -- A unique name
                        TEAM VARCHAR(50) NOT NULL,
                        DOMAIN_NAME VARCHAR(50) NOT NULL,
                        SUBNET VARCHAR(50) NOT NULL,
                        GATEWAY VARCHAR(50) NOT NULL,
                        DNS_SERVER1 VARCHAR(50) NOT NULL,
                        NIC VARCHAR(50) NOT NULL,
                        CREATED_FLAG INTEGER NOT NULL,
                        CREATED_FLAG_C INTEGER NOT NULL, -- Created/Edited flag
                        CREATED_VMS_FLAG INTEGER NOT NULL, -- I don't need it anymore
                        CONFIGURED_VMS_FLAG INTEGER NOT NULL, --
                        CONSTRAINT users_pk PRIMARY KEY(ID)
                        """
                        debugMessage(str(i) + "- " + str(team))

                    if int(TOTAL_VMS) > int(TOTAL_CREATED_VMS):
                        if int(UNIX_VMS) > int(TOTAL_CREATED_VMS):
                            # Stop creating UNIX VMs
                            vmtype = "Unix VM"
                        else:
                            # Create Win VMs
                            vmtype = "Windows VM"

                        # Get how many Win VM and Unix.
                        return render_template('competitions_vm_add.html', username=session['username'],
                                               templates_length=getTemplatesLength(), tasks_length=getEventsLength(),
                                               COMPETITION_NAME=COMPETITION_NAME, TEAM=TEAM, vmtype=vmtype)
            except Exception as e:
                if debug:
                    debugMessage(e)
                    debugMessage("NOTE: We don't need to config a tame ")
                    debugMessage("Block #1987823")
        elif request.form["step"] == "PAGE_3_PROCESS":
            pass
        elif request.form["step"] == "step_f":
            pass
        else:
            print("None of these steps is valid", file=sys.stderr)
            debugMessage("Redirect #1337912")
            return root()
    debugMessage("No session competitions_wizard()")
    debugMessage("Redirect #812323613")
    return root()


def competitions_wizard_summary_function(COMPETITION_NAME):
    if len(COMPETITION_NAME) < 1:
        if debug:
            error_message = "Missing COMPETITION_NAME in competitions_wizard_summary_function()"
            debugMessage(error_message)
        return render_template('error.html', message=error_message, url=url_for('competitions_team'),
                               templates_length=getTemplatesLength(), tasks_length=getEventsLength())

    comp1 = create_a_competition(COMPETITION_NAME)

    return render_template("wizard.html", username=session['username'], step="READY", COMPETITION_NAME=COMPETITION_NAME,
                           TEAMS=TEAMS, VMS=VMS)


@app.route("/competitions_wizard_summary", methods=['GET', 'POST'])
def competitions_wizard_summary():
    if 'username' in session:
        # Note that we are not calling this function plain "random()" because random
        # is the name of a package we imported.
        # Step 1, Create a comp

        if "step" not in request.form:
            """
            Doesn't take anything
            Sends a page where users can send the application back a new comp data.
            """
            debugMessage("Redirect #91243432233")
            return render_template("wizard.html")
        elif request.form["step"] == "READY":
            try:
                pass
            except Exception as e:
                if debug:
                    debugMessage(e)
                    debugMessage("NOTE: We don't need to config a tame ")
                    debugMessage("Block #19823243237823")
                pass
    debugMessage("No session competitions_wizard_summary()")
    debugMessage("Redirect #81324324377654613")
    return root()