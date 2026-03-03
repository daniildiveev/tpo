import pytest

from domain_model import (
    Arthur, Building, Crowd, Floor, People, Platform, Speaker, Window,
)


@pytest.fixture
def building():
    return Building(name="Здание")

@pytest.fixture
def second_floor(building):
    return Floor(number=2, building=building)

@pytest.fixture
def magnificent_window(second_floor):
    return Window(floor=second_floor, is_magnificent=True)

@pytest.fixture
def platform(magnificent_window):
    return Platform(window=magnificent_window)

@pytest.fixture
def people():
    return People(name="народ")

@pytest.fixture
def speaker(platform):
    return Speaker(name="Оратор", platform=platform)

@pytest.fixture
def arthur():
    return Arthur(name="Артур")

@pytest.fixture
def crowd():
    return Crowd(size=100)


class TestEntityCreation:

    def test_building_created(self, building):
        assert building.name == "Здание"

    def test_floor_created(self, second_floor, building):
        assert second_floor.number == 2
        assert second_floor.building is building

    def test_window_created_not_magnificent(self, second_floor):
        w = Window(floor=second_floor, is_magnificent=False)
        assert w.is_magnificent is False
        assert w.floor is second_floor

    def test_window_created_magnificent(self, magnificent_window, second_floor):
        assert magnificent_window.is_magnificent is True
        assert magnificent_window.floor is second_floor

    def test_platform_created(self, platform, magnificent_window):
        assert platform.window is magnificent_window

    def test_people_created(self, people):
        assert people.name == "народ"

    def test_people_default_name(self):
        p = People()
        assert p.name == "народ"

    def test_speaker_created(self, speaker, platform):
        assert speaker.name == "Оратор"
        assert speaker.platform is platform

    def test_arthur_created(self, arthur):
        assert arthur.name == "Артур"
        assert arthur.target_window is None
        assert arthur.is_sliding is False

    def test_crowd_created(self, crowd):
        assert crowd.size == 100
        assert crowd.is_cheering is False


class TestValidation:

    def test_floor_zero_raises(self, building):
        with pytest.raises(ValueError, match="≥ 1"):
            Floor(number=0, building=building)

    def test_floor_negative_raises(self, building):
        with pytest.raises(ValueError):
            Floor(number=-3, building=building)

    def test_floor_minimum_valid(self, building):
        f = Floor(number=1, building=building)
        assert f.number == 1

    def test_building_empty_name_raises(self):
        with pytest.raises(ValueError):
            Building(name="")

    def test_building_whitespace_name_raises(self):
        with pytest.raises(ValueError):
            Building(name="   ")

    def test_people_empty_name_raises(self):
        with pytest.raises(ValueError):
            People(name="")

    def test_speaker_empty_name_raises(self, platform):
        with pytest.raises(ValueError):
            Speaker(name="", platform=platform)

    def test_crowd_negative_size_raises(self):
        with pytest.raises(ValueError, match="≥ 0"):
            Crowd(size=-1)

    def test_crowd_zero_size_is_valid(self):
        c = Crowd(size=0)
        assert c.size == 0

    def test_floor_wrong_building_type_raises(self):
        with pytest.raises(TypeError):
            Floor(number=1, building="not a building")

    def test_window_wrong_floor_type_raises(self):
        with pytest.raises(TypeError):
            Window(floor="not a floor")

    def test_platform_wrong_window_type_raises(self):
        with pytest.raises(TypeError):
            Platform(window="not a window")

    def test_speaker_wrong_platform_type_raises(self):
        with pytest.raises(TypeError):
            Speaker(name="X", platform="not a platform")

    def test_arthur_empty_name_raises(self):
        with pytest.raises(ValueError):
            Arthur(name="")


class TestRelationshipIntegrity:

    def test_window_references_floor(self, magnificent_window, second_floor):
        assert magnificent_window.floor is second_floor

    def test_floor_references_building(self, second_floor, building):
        assert second_floor.building is building

    def test_window_transitively_references_building(self, magnificent_window, building):
        assert magnificent_window.floor.building is building

    def test_platform_references_window(self, platform, magnificent_window):
        assert platform.window is magnificent_window

    def test_speaker_references_platform(self, speaker, platform):
        assert speaker.platform is platform

    def test_speaker_transitively_references_window(self, speaker, magnificent_window):
        assert speaker.platform.window is magnificent_window


class TestArthurSlide:

    def test_slide_sets_target_window(self, arthur, magnificent_window):
        arthur.slide_toward(magnificent_window)
        assert arthur.target_window is magnificent_window

    def test_slide_sets_is_sliding_true(self, arthur, magnificent_window):
        assert arthur.is_sliding is False
        arthur.slide_toward(magnificent_window)
        assert arthur.is_sliding is True

    def test_slide_toward_non_magnificent_raises(self, arthur, second_floor):
        plain_window = Window(floor=second_floor, is_magnificent=False)
        with pytest.raises(ValueError, match="magnificent"):
            arthur.slide_toward(plain_window)

    def test_slide_toward_non_window_raises(self, arthur):
        with pytest.raises(TypeError):
            arthur.slide_toward("not a window")

    def test_slide_does_not_change_name(self, arthur, magnificent_window):
        original_name = arthur.name
        arthur.slide_toward(magnificent_window)
        assert arthur.name == original_name

    def test_slide_can_change_target(self, arthur, second_floor):
        w1 = Window(floor=second_floor, is_magnificent=True)
        w2 = Window(floor=second_floor, is_magnificent=True)
        arthur.slide_toward(w1)
        arthur.slide_toward(w2)
        assert arthur.target_window is w2


class TestSpeakerAddress:

    def test_address_returns_string(self, speaker, people):
        result = speaker.address(people)
        assert isinstance(result, str)

    def test_address_contains_speaker_name(self, speaker, people):
        result = speaker.address(people)
        assert speaker.name in result

    def test_address_contains_audience_name(self, speaker, people):
        result = speaker.address(people)
        assert people.name in result

    def test_address_wrong_type_raises(self, speaker):
        with pytest.raises(TypeError):
            speaker.address("not people")

    def test_speaker_can_address_different_audiences(self, speaker):
        p1 = People(name="толпа")
        p2 = People(name="народ")
        r1 = speaker.address(p1)
        r2 = speaker.address(p2)
        assert "толпа" in r1
        assert "народ" in r2

    def test_speaker_exists_without_addressing(self, speaker):
        assert speaker.name == "Оратор"


class TestCrowdErupt:

    def test_erupt_sets_is_cheering_true(self, crowd):
        assert crowd.is_cheering is False
        crowd.erupt()
        assert crowd.is_cheering is True

    def test_erupt_idempotent(self, crowd):
        crowd.erupt()
        crowd.erupt()
        assert crowd.is_cheering is True

    def test_empty_crowd_erupt_raises(self):
        empty = Crowd(size=0)
        with pytest.raises(ValueError, match="empty"):
            empty.erupt()

    def test_single_member_crowd_can_erupt(self):
        c = Crowd(size=1)
        c.erupt()
        assert c.is_cheering is True

    def test_erupt_does_not_change_size(self, crowd):
        original_size = crowd.size
        crowd.erupt()
        assert crowd.size == original_size


class TestFullNarrativeScenario:

    def test_full_scene(self):
        building = Building(name="Здание")
        floor    = Floor(number=2, building=building)
        window   = Window(floor=floor, is_magnificent=True)
        platform = Platform(window=window)

        people  = People(name="народ")
        speaker = Speaker(name="Оратор", platform=platform)
        arthur  = Arthur(name="Артур")
        crowd   = Crowd(size=500)

        crowd.erupt()
        arthur.slide_toward(window)
        speech = speaker.address(people)

        assert window.floor.number == 2
        assert window.floor.building is building
        assert window.is_magnificent is True
        assert platform.window is window

        assert speaker.platform is platform
        assert "Оратор" in speech
        assert "народ" in speech

        assert arthur.is_sliding is True
        assert arthur.target_window is window

        assert crowd.is_cheering is True

    def test_scene_building_floor_window_chain(self):
        b = Building(name="Дворец")
        f = Floor(number=2, building=b)
        w = Window(floor=f, is_magnificent=True)
        assert w.floor.building.name == "Дворец"

    def test_speaker_on_platform_before_window(self):
        b = Building(name="Б")
        f = Floor(number=2, building=b)
        w = Window(floor=f, is_magnificent=True)
        p = Platform(window=w)
        s = Speaker(name="С", platform=p)
        assert s.platform.window is w

    def test_arthur_targets_second_floor_window(self):
        b = Building(name="Б")
        f = Floor(number=2, building=b)
        w = Window(floor=f, is_magnificent=True)
        a = Arthur(name="Артур")
        a.slide_toward(w)
        assert a.target_window.floor.number == 2


class TestEdgeCases:

    def test_multiple_windows_on_same_floor(self, second_floor):
        windows = [Window(floor=second_floor, is_magnificent=True) for _ in range(5)]
        assert len(windows) == 5
        for w in windows:
            assert w.floor is second_floor

    def test_arthur_targets_exactly_one_window(self, second_floor):
        w1 = Window(floor=second_floor, is_magnificent=True)
        w2 = Window(floor=second_floor, is_magnificent=True)
        a  = Arthur(name="Артур")
        a.slide_toward(w1)
        assert a.target_window is w1
        assert a.target_window is not w2

    def test_floor_1_is_valid_boundary(self, building):
        f = Floor(number=1, building=building)
        assert f.number == 1

    def test_floor_high_number_is_valid(self, building):
        f = Floor(number=100, building=building)
        assert f.number == 100

    def test_crowd_large_size(self):
        c = Crowd(size=1_000_000)
        c.erupt()
        assert c.is_cheering is True

    def test_speaker_without_audience_no_error(self, platform):
        s = Speaker(name="Молчун", platform=platform)
        assert s.name == "Молчун"

    def test_plain_window_not_reachable_by_arthur(self, second_floor):
        plain = Window(floor=second_floor, is_magnificent=False)
        a = Arthur(name="Артур")
        with pytest.raises(ValueError):
            a.slide_toward(plain)
        assert a.is_sliding is False
        assert a.target_window is None
