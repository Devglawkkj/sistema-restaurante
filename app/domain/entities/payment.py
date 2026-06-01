from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class PaymentMethod(str, Enum):
    dinheiro = "dinheiro"
    cartao_credito = "cartao_credito"
    cartao_debito = "cartao_debito"
    pix = "pix"


@dataclass
class Payment:
    id: str
    comanda_id: str
    valor: float
    metodo: PaymentMethod
    data_pagamento: datetime
