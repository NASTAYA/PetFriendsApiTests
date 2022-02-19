from api import PetFriends
from settings import *


class TestPetFriends:
    def setup(self):
        self.pf = PetFriends()

    def test_successful_create_new_pet_without_photo(self, name='КУК', animal_type='кок', age=95):
        _, auth_key = self.pf.get_API_key(valid_email, valid_password)
        status, result = self.pf.create_new_pet_without_photo(auth_key, name, animal_type, age)
        assert status == 200
        assert result['name'] == name

    def test_successful_add_pet_photo(self, pet_photo='images/kok.jpg'):
        _, auth_key = self.pf.get_API_key(valid_email, valid_password)
        _, myPets = self.pf.get_list_of_pets(auth_key, "my_pets")

        if len(myPets['pets']) > 0:
            status, result = self.pf.add_pet_photo(auth_key, myPets['pets'][0]['id'], pet_photo)
            assert status == 200
            assert result['pet_photo'] != ""
        else:
            raise Exception("There is no my pets")

    def test_unsuccessful_add_invalid_pet_photo(self, pet_photo='images/photo.rtf'):
        _, auth_key = self.pf.get_API_key(valid_email, valid_password)
        _, myPets = self.pf.get_list_of_pets(auth_key, "my_pets")

        if len(myPets['pets']) > 0:
            status, result = self.pf.add_pet_photo(auth_key, myPets['pets'][0]['id'], pet_photo)
            assert status != 200
        else:
            raise Exception("There is no my pets")

    def test_unsuccessful_get_api_key_for_invalid_email(self, email=invalid_email, password=valid_password):
        status, result = self.pf.get_API_key(email, password)
        assert status == 403
        assert "This user wasn't found in database" in result

    def test_unsuccessful_get_apy_key_for_invalid_password(self, email=valid_email, password=invalid_password):
        status, result = self.pf.get_API_key(email, password)
        assert status == 403
        assert "This user wasn't found in database" in result

    def test_unsuccessful_get_all_pets_with_invalid_key(self, filter=''):  # filter available values : my_pets
        auth_key = invalid_key
        status, result = self.pf.get_list_of_pets(auth_key, filter)
        assert status == 403
        assert "Please provide 'auth_key" in result

    def test_try_successful_update_invalid_age(self, name='Мурзик', animal_type='Котэ', age=-99999999999999999999):
        _, auth_key = self.pf.get_API_key(valid_email, valid_password)
        _, myPets = self.pf.get_list_of_pets(auth_key, "my_pets")

        if len(myPets['pets']) > 0:
            status, result = self.pf.update_pet_info(auth_key, myPets['pets'][0]['id'], name, animal_type, age)
            assert status == 200
            print(' БАГ :ПОЛЕ ВОЗРАСТ ПРИНИМАЕТ ОТРИЦАТЕЛЬНЫЕ ЗНАЧЕНИЯ И НЕВОЗМОЖНЫЕ ЗНАЧЕНИЯ !!!!')
        else:
            raise Exception("There is no my pets")

    def test_try_successful_delete_not_my_pet(self):
        _, auth_key = self.pf.get_API_key(valid_email, valid_password)
        _, allPets = self.pf.get_list_of_pets(auth_key, '')
        _, myPets = self.pf.get_list_of_pets(auth_key, "my_pets")

        if len(myPets['pets']) == 0:
            self.pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
            _, myPets = self.pf.get_list_of_pets(auth_key, "my_pets")
        n = 0
        pet_id = allPets['pets'][n]['id']
        if pet_id in myPets.values():
            n += 1
        status, _ = self.pf.delete_pet(auth_key, pet_id)
        _, allPets = self.pf.get_list_of_pets(auth_key, '')
        assert status == 200
        assert pet_id not in allPets.values()
        print(' БАГ: САЙТ ПОЗВОЛЯЕТ УДАЛЯТЬ НЕ СВОИХ ПИТОМЦЕВ !!!!')

    def test_try_successful_delete_invalid_pet_id(self):
        _, auth_key = self.pf.get_API_key(valid_email, valid_password)
        pet_id = invalid_pet_id
        status, _ = self.pf.delete_pet(auth_key, pet_id)
        assert status == 200
        print(f' БАГ: Попытка удаления питомца  с некорректными значениями id = {pet_id} - возвращает успешный ответ !!!')

    def test_try_unsuccessful_delete_empty_pet_id(self):
        _, auth_key = self.pf.get_API_key(valid_email, valid_password)
        pet_id = empty_pet_id
        status, _ = self.pf.delete_pet(auth_key, pet_id)
        assert status == 400 or 404
        print(f'Попытка удалить питомца  с пустым значениями id не удалась')


    def test_try_successful_update_not_my_pet(self, name='Квадрат', animal_type='фигура', age='вечность'):
        _, auth_key = self.pf.get_API_key(valid_email, valid_password)
        _, allPets = self.pf.get_list_of_pets(auth_key, '')
        _, myPets = self.pf.get_list_of_pets(auth_key, "my_pets")

        if len(myPets['pets']) == 0:
            self.pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
            _, myPets = self.pf.get_list_of_pets(auth_key, "my_pets")
        n = 0
        pet_id = allPets['pets'][n]['id']
        if pet_id in myPets.values():
            n += 1
        status, result = self.pf.update_pet_info(auth_key, allPets['pets'][n]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
        print(f' БАГ: САЙТ ПОЗВОЛЯЕТ ИЗМЕНЯТЬ ДАННЫЕ НЕ СВОИХ ПИТОМЦЕВ !!!!')









