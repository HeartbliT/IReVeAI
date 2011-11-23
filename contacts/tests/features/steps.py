import sys

from lettuce import step, world, before

sys.path.append("../../../")

from newebe.lib.slugify import slugify

from newebe.contacts.models import Contact, ContactManager
from newebe.activities.models import ActivityManager
from newebe.settings import TORNADO_PORT

from newebe.contacts.models import STATE_WAIT_APPROVAL, STATE_TRUSTED
from newebe.contacts.models import STATE_PENDING

from newebe.lib.test_util import NewebeClient


ROOT_URL = "http://localhost:%d/" % TORNADO_PORT
SECOND_NEWEBE_ROOT_URL = "http://localhost:%d/" % (TORNADO_PORT + 10)

@before.all
def set_browser():
    world.browser = NewebeClient()
    world.browser.set_default_user()
    world.browser.login("password")

@step(u'Convert default user to contact')
def convert_default_user_to_contact(step):
    world.contact = world.user.asContact()

@step(u'Check that contact has same properties as default user')
def check_that_contact_has_same_properties_as_default_user(step):
    assert world.user.url == world.contact.url
    assert world.user.key == world.contact.key
    assert world.user.name == world.contact.name
    assert world.user.description == world.contact.description

@step(u'Deletes contacts')
def deletes_contacts(step):
    contacts = ContactManager.getContacts()
    while contacts:
        for contact in contacts:
            contact.delete()
        contacts = ContactManager.getContacts()

@step(u'Creates contacts')
def creates_contacts(step):
    contact = Contact()
    contact.url = "http://localhost/1/"
    contact.slug = slugify(contact.url)
    contact.state = STATE_PENDING
    contact.key = "key1"
    contact.save()
    contact2 = Contact()
    contact2.url = "http://localhost/2/"
    contact2.slug = slugify(contact.url)
    contact2.state = STATE_TRUSTED
    contact2.key = "key2"
    contact2.save()
    contact3 = Contact()
    contact3.url = "http://localhost/3/"
    contact3.slug = slugify(contact.url)
    contact3.state = STATE_WAIT_APPROVAL
    contact.key = "key3"
    contact3.save()

@step(u'Get contacts')
def get_contacts(step):
    world.contacts = ContactManager.getContacts()

@step(u'Check that there is (\d+) contacts')
def check_that_there_is_x_contacts(step, nb_contacts):
    assert int(nb_contacts) == len(world.contacts)

@step(u'Get requested contacts')
def get_requested_contacts(step):
    world.contacts = ContactManager.getRequestedContacts()

@step(u'Get pending contacts')
def get_pending_contacts(step):
    world.contacts = ContactManager.getPendingContacts()
    
@step(u'Get trusted contacts')
def get_trusted_contacts(step):
    world.contacts = ContactManager.getTrustedContacts()

@step(u'Get contact with slug : ([0-9a-z-]+)')
def get_contact_with_slug(step, slug):
    world.contact = ContactManager.getContact(slug)
    
@step(u'Check contact is null')
def check_contact_is_null(step):
    assert world.contact is None

@step(u'Check contact is not null')
def check_contact_is_not_null(step):
    assert world.contact is not None

@step(u'Get trusted contact with key : ([0-9a-z-]+)')
def get_trusted_contact_with_key(step, key):
    world.contact = ContactManager.getTrustedContact(key)


# Retry

@step(u'Set default contact')
def set_default_contact(step):
    world.contact = Contact()
    world.contact.name = "John Doe"
    world.contact.url = SECOND_NEWEBE_ROOT_URL       
    world.contact.slug = slugify(world.contact.url)
    
@step(u'Set contact with state as ERROR')
def set_contact_with_state_as_error(step):
    world.contact.state = "ERROR"
    world.contact.save()

@step(u'Send a retry request for this contact')
def send_a_retry_request_for_this_contact(step):
    
    world.response = world.browser.post(ROOT_URL + "contacts/" + \
                                world.contact._id + "/retry/",
                                '{"id":"%s"}' % world.contact._id)
    assert world.response.code == 200

@step(u'Checks that contact state is PENDING')
def checks_that_contact_state_is_pending(step):
    contact = ContactManager.getContact(world.contact.slug)
    assert contact.state == "PENDING"    

@step(u'Checks that second newebe has first newebe in contact')
def checks_that_second_newebe_has_first_newebe_in_contact(step):
    contacts = world.browser.fetch_documents_from_url(
            SECOND_NEWEBE_ROOT_URL + "contacts/pending/")
    assert len(contacts) == 1
    second_newebe_contact = contacts[0]
    assert second_newebe_contact["slug"] == slugify(ROOT_URL)


## Handlers

@step(u'Through handler retrieve requested contacts')
def through_handler_retrieve_requested_contacts(step):
    world.contacts = world.browser.fetch_documents(
            "contacts/requested/")

@step(u'Through handlers retrieve pending contacts')
def through_handlers_retrieve_pending_contacts(step):
    world.contacts = world.browser.fetch_documents(
            "contacts/pending/")

@step(u'Through handlers retrieve trusted contacts')
def through_handlers_retrieve_trusted_contacts(step):
    world.contacts = world.browser.fetch_documents(
            "contacts/trusted/")



@step(u'Create a default contact')
def create_a_default_contact(step):
    contact = Contact()
    contact.url = u"http://default:8000/"
    contact.slug = slugify(contact.url)
    contact.state = STATE_TRUSTED
    contact.description = "desc 1"
    contact.name = "default contact 1"
    contact.save()

@step(u'Change default contact data through handlers')
def change_default_contact_data_through_handlers(step):
    contact = ContactManager.getContact(slugify(u"http://default:8000/"))
    contact.description = "desc 2"
    contact.url = u"http://default:8010/"
    contact.name = "default contact 2"
    world.browser.put(ROOT_URL + "contacts/update-profile/", contact.toJson())
    
@step(u'Checks that default contact data are updated')
def checks_that_default_contact_data_are_updated(step):
    contact = ContactManager.getContact(slugify(u"http://default:8000/"))
    assert "http://default:8010/" == contact.url
    assert "default contact 2" == contact.name
    assert "desc 2" == contact.description

@step(u'Checks that contact update activity is properly created')
def checks_that_contact_update_activity_is_properly_created(step):
    activity = ActivityManager.get_all().first()
    assert "modifies" == activity.verb
    assert "profile" == activity.docType
    assert False == activity.isMine
    assert "default contact 2"  == activity.author

