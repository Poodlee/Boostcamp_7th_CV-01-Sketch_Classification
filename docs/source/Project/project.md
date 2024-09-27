# Project 

## 프로젝트 팀 구성 및 역할

* Team Member 1: 데이터 수집 및 전처리
* Team Member 2: 모델링 및 학습
* Team Member 3: 결과 분석 및 평가
* Team Member 4: 프로젝트 관리 및 보고서 작성


### 팀원들 한줄평 



## 수행 절차 및 방법 

### Step 1: 데이터 수집 및 전처리
* 데이터를 다양한 소스로부터 수집하고, 결측치 및 이상치를 처리하여 학습에 적합한 형식으로 정제합니다.
* 예를 들어, 결측치를 처리하는 코드:
    ```python
    import pandas as pd

    # 데이터 로드
    data = pd.read_csv('data.csv')

    # 결측치 처리
    data.fillna(method='ffill', inplace=True)
    ```

### Step 2: 데이터 탐색 및 시각화
* 수집된 데이터를 분석하고 다양한 시각화 기법을 통해 데이터의 특징과 분포를 파악합니다.
* 예를 들어, 데이터의 분포를 히스토그램으로 시각화:
    ```python
    import matplotlib.pyplot as plt

    # 데이터 분포 시각화
    plt.hist(data['feature_column'], bins=30)
    plt.title('Feature Distribution')
    plt.show()
    ```

### Step 3: 모델 학습
* 다양한 딥러닝 모델을 적용하여 최적의 성능을 가진 모델을 학습합니다.
    ```python

    def train(trainer_mod, data_mod,my_loggers,checkpoint_callback,**hparams):
        trainer = pl.Trainer(
            logger=my_loggers,
            accelerator="cpu" if hparams['gpus'] == 0 else "gpu",
            precision=16 if hparams['gpus'] != 0 else 32,  # CPU에서는 32-bit precision
            devices=None if hparams['gpus'] == 0 else hparams['gpus'],
            callbacks=checkpoint_callback,  # 콜백 리스트로 묶는 것이 좋음
            max_epochs=hparams['epochs'],
            accumulate_grad_batches=(1 if hparams['accumulate_grad_batches'] <= 0
                else hparams['accumulate_grad_batches']),
        )

        trainer.fit(trainer_mod, data_mod)

        return trainer,trainer_mod,data_mod


    data_mod = data_module.SketchDataModule(**hparams)
    trainer_mod = Sketch_Classifier(**hparams)
    trainer,trainer_mod, data_mod = train(trainer_mod, data_mod,my_loggers,checkpoint_callback,**hparams)
    ```

### Step 4: 모델 평가
* 학습된 모델을 평가하고, 성능을 측정하기 위한 다양한 지표를 사용합니다.
    ```python
    def val_pred(trainer,trainer_mod,data_mod,**hparams):

        data_mod.test_data_dir = data_mod.train_data_dir
        data_mod.test_info_df = data_mod.val_info_df
        data_mod.setup(stage="predict")

        validations = trainer.predict(trainer_mod, dataloaders=data_mod.predict_dataloader())

        pred_list = []

        for batch in validations:
            if hparams['kfold_pl_train_return']:
                preds, logits = batch  
            else:
                preds = batch 
            pred_list.extend(preds.cpu().numpy())  
   
    return pred_list#,logit_list # kfold 수행 시
    ```

### Step 5: 하이퍼파라미터 튜닝
* 모델의 성능을 향상시키기 위해 wandb의 sweep을 이용하여하이퍼파라미터(예: 학습률, 배치 크기, 네트워크 구조 등)를 조정하고 최적의 설정을 찾습니다.
    ```python
    def run_sweep():
        sweep_config = {
            "name": "ResnextTesting",
            "method": "bayes", # random -> bayes 
            "metric": {"goal": "minimize", "name": "valid_loss_epoch"},
            "parameters": {
                "learning_rate": {"min": 0.00001, "max": 0.001},
                "batch_size": {"values": [32, 64, 128]},
                "optimizer": {"values": ["AdamW", "SGD"]},
                "loss": {"values": ["Focal", "CE"]},
                "label_smoothing": {
                    "values": [0.0, 0.1, 0.2, 0.3],
                    #"condition": {"loss": "CE"}  # 조건 설정
                },
                # "focal_constant": {
                #     "alpha_val": [0.1, 0.25, 0.5, 0.75, 1.0],
                #     "gamma_val": [0.0, 1.0, 2.0, 3.0, 5.0],
                #     "condition": {"loss": "focal"}
                # },
                "focal_alpha": {
                    "values": [0.1, 0.25, 0.5, 0.75, 1.0],
                    #"condition": {"loss": "Focal"}  # 조건 설정
                },
                "focal_gamma": {
                    "values":[0.0, 1.0, 2.0, 3.0, 5.0],
                    #"condition": {"loss": "Focal"}
                },
                "cutmix_ratio": {"min": 0.1, "max": 0.4},
                "mixup_ratio": {"min": 0.1, "max": 0.4},
            },
        }
        sweep_id = wandb.sweep(sweep_config, project="sketch classification", entity="nav_sketch")
        wandb.agent(sweep_id, function=lambda: main(args), count=1) # 각 모델에 대해 한 번씩 실행
    ```

### Step 6: 결과 분석 및 시각화
* GradCAM 이용하여 시각화 진행
    <p align="center">
    <img src="https://github.com/user-attachments/assets/301a97b9-2caf-4ae2-a895-17ee0b1a5711" alt="image" width="300"/>
    </p>

### 수행 결과 
* 전체적인 평가, 분석 내용 