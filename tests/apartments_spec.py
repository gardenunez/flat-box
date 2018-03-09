from doublex import Stub, ANY_ARG
from expects import expect, equal
from mamba import description, it

from apartments import get_apartments

with description("Apartments Spec"):
    with it("returns empty list"):
        with Stub() as db:
            db.execute_query(ANY_ARG).returns([])
        expect(get_apartments(db=db)).to(equal([]))
