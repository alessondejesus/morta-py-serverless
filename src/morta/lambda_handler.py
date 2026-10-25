from mangum import Mangum

from morta.main import app

handler = Mangum(app)
