import json
import base64
from rest_framework.test import APITestCase
from django.utils import timezone
from people.models import Person


class WebhookTestCase(APITestCase):
    def setUp(self):
        self.new_bounced_person = Person.objects.create_person(
            email='new@bounce.com',
            created=timezone.now()
        )

        self.old_bounced_person = Person.objects.create_person(
            email='old@bounce.com',
            created=timezone.now() - timezone.timedelta(hours=2)
        )

        self.nb_payload = json.loads('{"nation_slug":"plp","payload":{"person":{"birthdate":null,"city_district":null,"civicrm_id":null,"county_district":null,"county_file_id":null,"created_at":"2017-07-07T16:14:47+02:00","datatrust_id":null,"do_not_call":false,"do_not_contact":false,"dw_id":null,"email":"new@nb.com","email_opt_in":true,"employer":null,"external_id":null,"federal_district":null,"fire_district":null,"first_name":"Prénom","has_facebook":false,"id":1163361,"is_twitter_follower":false,"is_volunteer":false,"judicial_district":null,"labour_region":null,"last_name":"Nom","linkedin_id":null,"mobile":null,"mobile_opt_in":false,"nbec_guid":null,"ngp_id":null,"note":null,"occupation":null,"party":null,"pf_strat_id":null,"phone":null,"precinct_id":null,"primary_address":null,"profile_image_url_ssl":"https://d3n8a8pro7vhmx.cloudfront.net/assets/icons/buddy.png","recruiter_id":null,"rnc_id":null,"rnc_regid":null,"salesforce_id":null,"school_district":null,"school_sub_district":null,"sex":null,"signup_type":0,"state_file_id":null,"state_lower_district":null,"state_upper_district":null,"support_level":null,"supranational_district":null,"tags":[],"twitter_id":null,"twitter_name":null,"updated_at":"2017-07-07T16:14:47+02:00","van_id":null,"village_district":null,"ward":null,"work_phone_number":null,"active_customer_expires_at":null,"active_customer_started_at":null,"author":null,"author_id":null,"auto_import_id":null,"availability":null,"ballots":[],"banned_at":null,"billing_address":null,"bio":null,"call_status_id":null,"call_status_name":null,"capital_amount_in_cents":0,"children_count":0,"church":null,"city_sub_district":null,"closed_invoices_amount_in_cents":null,"closed_invoices_count":null,"contact_status_id":null,"contact_status_name":null,"could_vote_status":false,"demo":null,"donations_amount_in_cents":0,"donations_amount_this_cycle_in_cents":0,"donations_count":0,"donations_count_this_cycle":0,"donations_pledged_amount_in_cents":0,"donations_raised_amount_in_cents":0,"donations_raised_amount_this_cycle_in_cents":0,"donations_raised_count":0,"donations_raised_count_this_cycle":0,"donations_to_raise_amount_in_cents":0,"email1":"aleianne@laposte.net","email1_is_bad":false,"email2":null,"email2_is_bad":false,"email3":null,"email3_is_bad":false,"email4":null,"email4_is_bad":false,"emails":[{"email_address":"aleianne@laposte.net","email_number":1,"is_bad":false,"is_primary":true}],"ethnicity":null,"facebook_address":null,"facebook_profile_url":null,"facebook_updated_at":null,"facebook_username":null,"fax_number":null,"federal_donotcall":false,"first_donated_at":null,"first_fundraised_at":null,"first_invoice_at":null,"first_prospect_at":null,"first_recruited_at":null,"first_supporter_at":"2017-07-07T16:14:47+02:00","first_volunteer_at":null,"full_name":"Virginia Sartoris","home_address":null,"import_id":null,"inferred_party":null,"inferred_support_level":null,"invoice_payments_amount_in_cents":null,"invoice_payments_referred_amount_in_cents":null,"invoices_amount_in_cents":null,"invoices_count":null,"is_absentee_voter":null,"is_active_voter":null,"is_deceased":false,"is_donor":false,"is_dropped_from_file":null,"is_early_voter":null,"is_fundraiser":false,"is_ignore_donation_limits":false,"is_leaderboardable":true,"is_mobile_bad":false,"is_permanent_absentee_voter":null,"is_possible_duplicate":false,"is_profile_private":false,"is_profile_searchable":true,"is_prospect":false,"is_supporter":true,"is_survey_question_private":false,"language":null,"last_call_id":null,"last_contacted_at":null,"last_contacted_by":null,"last_donated_at":null,"last_fundraised_at":null,"last_invoice_at":null,"last_rule_violation_at":null,"legal_name":null,"locale":null,"mailing_address":null,"marital_status":null,"media_market_name":null,"meetup_id":null,"meetup_address":null,"membership_expires_at":null,"membership_level_name":null,"membership_started_at":null,"middle_name":null,"mobile_normalized":"627036590","nbec_precinct_code":null,"nbec_precinct":null,"note_updated_at":null,"outstanding_invoices_amount_in_cents":null,"outstanding_invoices_count":null,"overdue_invoices_count":null,"page_slug":"rdv_ete_de_la_france_insoumise","parent":null,"parent_id":null,"party_member":null,"phone_normalized":null,"phone_time":null,"precinct_code":null,"precinct_name":null,"prefix":null,"previous_party":null,"primary_email_id":1,"priority_level":null,"priority_level_changed_at":null,"profile_content":null,"profile_content_html":null,"profile_headline":null,"received_capital_amount_in_cents":0,"recruiter":null,"recruits_count":0,"registered_address":null,"registered_at":null,"religion":null,"rule_violations_count":0,"signup_sources":[],"spent_capital_amount_in_cents":0,"submitted_address":null,"subnations":[],"suffix":null,"support_level_changed_at":null,"support_probability_score":null,"township":null,"turnout_probability_score":null,"twitter_address":null,"twitter_description":null,"twitter_followers_count":null,"twitter_friends_count":null,"twitter_location":null,"twitter_login":null,"twitter_updated_at":null,"twitter_website":null,"unsubscribed_at":null,"user_submitted_address":null,"username":null,"voter_updated_at":null,"warnings_count":0,"website":null,"work_address":null,"associations":null,"syndicat":null,"autres_engagements":null,"respo_politique":null,"parti_politique":null,"500_signatures":null,"metier":null,"genre":null,"contribution_convention":null,"bus_convention":null}},"token":"prout","version":4}')

        self.sendgrid_payload = [
            {
                "email": "new@bounce.com",
                "event": "bounce"
            },
            {
                "email": "old@bounce.com",
                "event": "bounce"
            }
        ]

        self.ses_payload = r'''{
              "Type" : "Notification",
              "MessageId" : "7ba9da19-da05-55b5-8074-8bc6e50cfdf1",
              "TopicArn" : "arn:aws:sns:eu-west-1:106475418133:jlm2017-newsletter-notification",
              "Message" : "{\"notificationType\":\"Bounce\",\"bounce\":{\"bounceType\":\"Permanent\",\"bounceSubType\":\"General\",\"bouncedRecipients\":[{\"emailAddress\":\"old@bounce.com\",\"action\":\"failed\",\"status\":\"5.1.1\",\"diagnosticCode\":\"smtp; 550 5.1.1 <old@bounce.com>: Recipient address rejected: User unknown in virtual mailbox table\"}],\"timestamp\":\"2017-07-11T21:02:01.056Z\",\"feedbackId\":\"0102015d3375711d-abd3f429-32f0-4ebe-81b9-f765e95ff3ba-000000\",\"remoteMtaIp\":\"217.70.184.6\",\"reportingMTA\":\"dsn; a6-144.smtp-out.eu-west-1.amazonses.com\"},\"mail\":{\"timestamp\":\"2017-07-11T21:01:59.000Z\",\"source\":\"nepasrepondre@lafranceinsoumise.fr\",\"sourceArn\":\"arn:aws:ses:eu-west-1:106475418133:identity/lafranceinsoumise.fr\",\"sourceIp\":\"163.172.170.222\",\"sendingAccountId\":\"106475418133\",\"messageId\":\"0102015d33756cb0-9ef9f3ed-65bb-4054-bd09-c3fc71aa19ba-000000\",\"destination\":[\"old@bounce.com\"]}}"
            }'''

    def test_nb(self):
        response = self.client.post('/webhooks/nb_add_person', self.nb_payload, format='json')
        self.assertEqual(response.status_code, 202)
        self.assertEqual('new@nb.com', Person.objects.get(email='new@nb.com').email)

    def test_nb_auth(self):
        self.nb_payload['token'] = 'wrong prout'
        response = self.client.post('/webhooks/nb_add_person', self.nb_payload, format='json')
        self.assertEqual(response.status_code, 401)

    def test_sendgrid_bounce_users(self):
        response = self.client.post('/webhooks/sendgrid_bounce', self.sendgrid_payload, format='json',
            HTTP_AUTHORIZATION='Basic ' + (base64.b64encode(b'fi:prout').decode('utf-8')))
        self.assertEqual(response.status_code, 202)
        self.assertEqual(True, Person.objects.get(email='old@bounce.com').bounced)
        with self.assertRaises(Person.DoesNotExist):
            Person.objects.get(email='new@bounce.com')

    def test_sendgrid_auth(self):
        response = self.client.post('/webhooks/sendgrid_bounce', self.sendgrid_payload, format='json',
            HTTP_AUTHORIZATION='Basic ' + (base64.b64encode(b'fi:burp').decode('utf-8')))
        self.assertEqual(response.status_code, 401)
        response = self.client.post('/webhooks/sendgrid_bounce', self.sendgrid_payload, format='json')
        self.assertEqual(response.status_code, 401)

    def test_amazon_bounce_old_user(self):
        response = self.client.post('/webhooks/ses_bounce', self.ses_payload,
            HTTP_AUTHORIZATION='Basic ' + (base64.b64encode(b'fi:prout').decode('utf-8')))
        self.assertEqual(response.status_code, 202)
        self.assertEqual(True, Person.objects.get(email='old@bounce.com').bounced)

    def test_amazon_auth(self):
        response = self.client.post('/webhooks/ses_bounce', self.ses_payload,
            HTTP_AUTHORIZATION='Basic ' + (base64.b64encode(b'fi:burp').decode('utf-8')))
        self.assertEqual(response.status_code, 401)
        response = self.client.post('/webhooks/ses_bounce', self.ses_payload)
        self.assertEqual(response.status_code, 401)
