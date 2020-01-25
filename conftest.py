def pytest_generate_tests(metafunc):
    from pytest_cleanup import parametrize_stg_tests

    parametrize_stg_tests(metafunc)


